#!/usr/bin/env python3
"""Check new_properties.xml with the PIM-X code itself (no GUI).

1. Evaluates every generator category of the XML at four volumes, as PIM-X "Rebuild Properties" does, and reports
   the categories that fail. Four placeholders are expected to fail (Network Enabling Dummy, Stoplight, RR Crossing,
   Effect): they are not meant to be used.
2. Optionally (--package), recomputes the building exemplars of an installed SC4SIM package and lists every
   building whose capacity, plop cost, monthly cost, jobs or coverage radius differ from what the XML gives. A package rebuilt
   with this XML reports no differences.

Usage:
    python check_pimx.py --pimx /path/to/sc4pim-x/src --xml new_properties.xml
    python check_pimx.py --pimx /path/to/sc4pim-x/src --xml new_properties.xml \
        --package "Plugins/050-load-first/cam.sc4-system-integration-module.stable.4.0.2.sc4pac" \
        --files CAM_Education_Buildings.dat CAM_Health_Buildings.dat CAM_Police_Fire_Buildings.dat \
                CAM_Power_Garbage_Buildings.dat CAM_Water_Buildings.dat

Exit code: 0 when everything matches, 1 when a category fails (other than the placeholders) or a building differs.
Requires Python 3.10+ and the PIM-X sources (https://github.com/caspervg/sc4pim-x); wxPython is not needed.
"""
import argparse
import glob
import importlib.abc
import importlib.machinery
import logging
import os
import pathlib
import sys
import types

# --- wxPython / OpenGL stand-ins: PIM-X imports them at module level, the generator code does not use them -------
class _Any(type):
    def __getattr__(cls, n):
        if n.startswith('__'):
            raise AttributeError(n)
        return _mk(n)

    def __or__(cls, o):
        return cls
    __ror__ = __or__


def _mk(name='Any'):
    return _Any(name, (object,), {'__init__': lambda self, *a, **k: None,
                                  '__getattr__': lambda self, n: _mk(n),
                                  '__call__': lambda self, *a, **k: _mk()})


class _StubModule(types.ModuleType):
    def __getattr__(self, n):
        if n.startswith('__'):
            raise AttributeError(n)
        v = _mk(n)
        setattr(self, n, v)
        return v


class _Finder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    PREFIX = ('wx', 'OpenGL', 'glcontext', 'moderngl')

    def find_spec(self, fullname, path, target=None):
        if fullname.split('.')[0] in self.PREFIX:
            return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
        return None

    def create_module(self, spec):
        m = _StubModule(spec.name)
        m.__path__ = []
        return m

    def exec_module(self, m):
        pass


PLACEHOLDERS = {'Network Enabling Dummy', 'Stoplight', 'RR Crossing', 'Effect'}
CHECKED = {0x8922041B: 'School Student Capacity', 0x69220415: 'Hospital Patient Capacity', 0x4AA60EBC: 'Catalog Capacity',
           0x49CAC341: 'Plop Cost', 0xEA54D286: 'Budget Item: Cost', 0x27812841: 'Demand Created',
           0x691B42B3: 'School Coverage Radius', 0x091B42A2: 'Hospital Coverage Radius',
           0x08F55DC2: 'Fire Station, Radius', 0x48D71ED2: 'Police Station, Radius'}


def load_pimx(src, xml):
    sys.meta_path.insert(0, _Finder())
    sys.path.insert(0, src)
    logging.disable(logging.CRITICAL)
    import sc4pimx.SC4VirtualDat as V
    V.data_file_path = lambda n: pathlib.Path(xml)
    vd = object.__new__(V.VirtualDat)
    for k, v in dict(properties={}, categories={}, builtin_family_names={}, lotStages={}, baseTex={}, zoning={},
                     rootCategory=None, MaxSlopeBeforeLotFoundation='90', MaxSlopeAllowed='90', allEntries=[],
                     TGIIndex={}).items():
        setattr(vd, k, v)
    vd.ReadProperties()
    return vd


def check_categories(vd):
    import sc4pimx.SC4PIMApp as A

    class NoExemplar:
        def GetProp(self, k):
            return None

    def leaves(c):
        if not c.childs:
            yield c
        for ch in c.childs:
            yield from leaves(ch)

    evaluated, failures = 0, []
    for cat in leaves(vd.rootCategory):
        total, p = len(cat.evalProperties) + len(cat.code), cat
        while p is not None and total == 0:
            total += len(p.evalProperties) + len(p.code)
            p = p.parent
        if not total:
            continue
        for vol in (500., 3000., 60000., 300000.):
            scope = dict(Height=10., Width=20., Depth=20., Volume=vol, volume=vol, LotSizeX=4, LotSizeY=4,
                         fillingDegree=0.5, IID=0x12345678, GID=0, exemplarName='x')
            evaluated += 1
            try:
                A.build_category_props_for_preset(vd, NoExemplar(), cat, scope)
            except Exception as e:  # noqa: BLE001 - report every failure
                failures.append((cat.Name, vol, '%s: %s' % (type(e).__name__, str(e)[:120])))
                break
    return evaluated, failures


def index_lots(vd, package):
    from sc4pimx.SC4DatTools import DatFile, SC4Exemplar

    class Lot:
        pass
    lots = {}
    for fn in glob.glob(os.path.join(package, '**', '*.dat'), recursive=True):
        try:
            df = DatFile(fn, None, True)
        except Exception:  # noqa: BLE001
            continue
        for e in df.entries:
            if e.tgi[0] != 0x6534284A:
                continue
            e.read_file(None)
            e.virtual_dat = vd
            try:
                ex = SC4Exemplar(e, vd)
            except Exception:  # noqa: BLE001
                continue
            t = ex.GetProp(0x10)
            if not t or t[0] != 0x10:
                continue
            for pid in range(0x88EDC900, 0x88EDCE00):
                v = ex.GetProp(pid)
                if v and v[0] == 0:
                    for iid in v[12:]:
                        if iid not in lots:
                            lot = Lot()
                            lot.exemplar = ex
                            lots[iid] = lot
    vd.FindLotFromBuilding = lambda bex: lots.get(bex.entry.tgi[2])


def check_package(vd, files):
    import sc4pimx.SC4Data as D
    import sc4pimx.SC4PIMApp as A
    from sc4pimx.SC4DatTools import DatFile, SC4Exemplar
    differences = []
    for fn in files:
        for e in DatFile(fn, None, True).entries:
            if e.tgi[0] != 0x6534284A:
                continue
            e.read_file(None)
            e.virtual_dat = vd
            try:
                ex = SC4Exemplar(e, vd)
            except Exception:  # noqa: BLE001
                continue
            t = ex.GetProp(0x10)
            if not t or t[0] != 2:
                continue
            e.exemplar = ex
            ok, cats = D.GetCategories(vd.rootCategory, D.BuildingDesc(e))
            if not ok or not cats:
                continue
            cat = vd.categories[cats[0][1]]
            try:
                fd = ex.GetProp(0x27812811)[0]
            except Exception:  # noqa: BLE001
                fd = 0.5
            try:
                rows = A.build_recompute_preview_rows(vd, ex, cat, 0, fd)
            except Exception as err:  # noqa: BLE001
                differences.append((os.path.basename(fn), ex.GetProp(0x20)[0], cat.Name, 'ERROR', str(err), ''))
                continue
            for r in rows:
                if r['id'] in CHECKED and r['status'] in (A.recomputePreviewStatusUpdate, A.recomputePreviewStatusAdd):
                    try:  # ignore float formatting (6581.96777 vs 6581.968)
                        if abs(float(r['current']) - float(r['recomputed'])) < 0.01:
                            continue
                    except (TypeError, ValueError):
                        pass
                    differences.append((os.path.basename(fn), ex.GetProp(0x20)[0], cat.Name, CHECKED[r['id']],
                                        r['current'], r['recomputed']))
    return differences


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pimx', required=True, help='PIM-X src folder (the one that contains sc4pimx/)')
    ap.add_argument('--xml', required=True, help='new_properties.xml to check')
    ap.add_argument('--package', help='installed SC4SIM package folder (lots are read from it)')
    ap.add_argument('--files', nargs='*', default=[], help='building DATs to compare (names inside --package or paths)')
    args = ap.parse_args()

    vd = load_pimx(os.path.abspath(args.pimx), os.path.abspath(args.xml))
    evaluated, failures = check_categories(vd)
    unexpected = [f for f in failures if f[0] not in PLACEHOLDERS]
    print('Categories: %d evaluations, %d failures (%d expected placeholders)' %
          (evaluated, len(failures), len(failures) - len(unexpected)))
    for name, vol, err in unexpected:
        print('  FAIL %-40s volume %-8g %s' % (name, vol, err))

    differences = []
    if args.package:
        index_lots(vd, args.package)
        files = []
        for f in args.files:
            if os.path.exists(f):
                files.append(f)
            else:
                found = glob.glob(os.path.join(args.package, '**', f), recursive=True)
                files.extend(p for p in found if 'Legacy' not in p)
        differences = check_package(vd, files)
        print('Package: %d files, %d differences from the XML' % (len(files), len(differences)))
        for fn, name, cat, prop, cur, new in differences:
            print('  %-32s %-40s %-22s %-24s %s -> %s' % (fn, name[:40], cat[:22], prop, str(cur)[:60], str(new)[:60]))

    sys.exit(1 if unexpected or differences else 0)


if __name__ == '__main__':
    main()
