# New_Properties.xml-patches

**The property definitions and lot generators for SimCity 4 modding tools, with a balanced civic and utility model for
CAM and SC4SIM.**

[![Latest tag](https://img.shields.io/github/v/tag/UlisseWolf/New_Properties.xml-patches?label=version)](https://github.com/UlisseWolf/New_Properties.xml-patches/tags)
![Game](https://img.shields.io/badge/SimCity%204-Deluxe%20%2F%20Rush%20Hour-green)
![Tools](https://img.shields.io/badge/tools-PIM--X%20%7C%20iLive%20Reader-blue)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](LICENSE)

`new_properties.xml` tells the SimCity 4 modding tools what every exemplar property means: its ID, name, type, allowed
values and description. It also holds the **generators** that compute the statistics of new lots (residential,
commercial, industrial, civic and utility buildings: capacity, costs, jobs, coverage, demand), the Transit-Enabled
switches and station capacities, and the occupant groups.

This repository is a fork of the [NAM Team's New_Properties.xml](https://github.com/NAMTeam/New_Properties.xml) with
faster updates, the properties of the newer DLL mods, and a public services model rebuilt on the Maxis buildings and on
real-world figures.

---

## Contents

- [Which version should I use?](#which-version-should-i-use)
- [Features](#features)
- [Installation](#installation)
- [Using it with PIM-X](#using-it-with-pim-x)
- [Civic and utility balance model](#civic-and-utility-balance-model)
- [Verification](#verification)
- [Repository layout](#repository-layout)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Which version should I use?

The two files share the same patches, additional buildings and DLL properties. They differ in the public services
model and in how quickly they are updated.

| | [NAM Team New_Properties.xml](https://github.com/NAMTeam/New_Properties.xml) | **New_Properties.xml-patches** (this repository) |
|---|---|---|
| Recommended for | Vanilla or hybrid vanilla games | CAM, CAM-SPAM, CAM-Vanilla and hybrid games |
| Public services (education, health, safety) | BSC Team values: half the Maxis capacities, so more buildings are needed | Capacities on the scale of real buildings, well above the BSC values; costs, coverage and jobs computed per resident served |
| Updates (new buildings and patches) | Later | First |
| SC4SIM features (deathcare, I-M zone, mixed use) | No | Yes |

## Features

**Public services and utilities**
- Education, health and safety rebuilt with one rule for every family: monthly cost per resident served at the Maxis
  level, plop cost as months of upkeep, coverage radius from the residents served, jobs on the Maxis and real-world
  scale (see the [balance model](#civic-and-utility-balance-model)).
- Education compatible with the Education Realism Mod (ERM) and CAM, with new buildings such as a kindergarten and a
  modular university.
- Utilities: new power plant types, electrical substations and batteries, power plant costs and staff by fuel, and the
  features Maxis removed brought back (fresh water pump, desalination plant, incinerator).
- Parks that cost what they give: monthly cost from their park effect, landmark effect and cap relief.

**Transport, farms and growables**
- Transit-Enabled (TE) buildings that follow the NAM-MTA specifications.
- Farm generators from SPAM and Colossus Farming, the BSC ones updated, and farms up to stage 10 (stages 4 and 5 need
  CAM or SPAM, stages 5 to 10 need CAM).
- The additional buildings and properties of the CAM expansions.

**Properties and occupant groups**
- Every occupant group of Maxis and the BSC Team, plus the recovered and new ones.
- The properties created by DLL mods, so the tools can read and write them and Lua scripts can use their IDs.

**SC4SIM integration** (needs [SC4SIM](https://github.com/UlisseWolf/SC4-System-Integration-Module))

| Feature | What the XML adds | Needs |
|---|---|---|
| Deathcare | Properties Deathcare Type, Capacity and Radius (`0x5C4DD001`-`0x5C4DD003`); occupant groups Crematorium (`0x5C4DD100`) and Cemetery (`0x5C4DD101`); Cemeteries (`0x5C4DD200`) and Crematoria (`0x5C4DD201`) submenus under Health; Cemetery and Crematorium generators under Hospital. The Reward Cemetery generator is unchanged. | SC4SIM.dll 1.9.4 or later |
| Manufacturing zone | Zone `0x0D` of LotConfigPropertyZoneTypes is shown as *I - Manufacturing* instead of Spaceport. | SC4SIM ManufacturingZone |
| Mixed-use growables | A Mixed-Use (R-C-I) category with residential, commercial and industrial groups, each also W2W (see below). | SC4SIM MixedOccupancy, SC4QueryUIHooks.dll |

<details>
<summary>Mixed-use growables in detail</summary>

- **Mixed-Use Residential**: homes above shops (R/CS $, $$, $$$), Live-Work (R/I-m $$) and Farmstead (R/I-a $).
- **Mixed-Use Commercial**: shops with apartments (CS/R $, $$, $$$) and offices with apartments (CO/R $$, $$$).
- **Mixed-Use Industrial**: Farm with Farmhouse (I-a/R $), Farm with Farmhouse and Farm Shop (I-a/R/CS $), Workshop
  with Flats (I-m/R $$) and Tech Campus (I-ht/R $$$).

Every generator sets *Allow Joint Occupancy* = true and gives the secondary uses the building's own wealth, the only
wealth the game fills. The query exemplars point to the mixed-use queries of CAM's `CAM_UI.dat`
(`0x5C4DE200`-`0x5C4DE20B`), which add rows with the occupancy and capacity of the secondary uses.

Occupant groups: *Building: Mixed-Use (R-C-I)* (`0x5C4DE000`, every mixed-use building), Mixed-Use Residential,
Commercial and Industrial (`0x5C4DE010`, `0x5C4DE020`, `0x5C4DE030`) and one per generator (`0x5C4DE011`-`0x5C4DE015`,
`0x5C4DE021`-`0x5C4DE025`, `0x5C4DE031`-`0x5C4DE034`), next to the usual R, C and I groups of each use.

</details>

## Installation

Download `new_properties.xml` (or `tropod_Properties.xml` for the old Reader) from this repository and put it where
your tool reads it, replacing the original file. Keep a copy of the original if you want to go back.

| Tool | File | Folder |
|---|---|---|
| **PIM-X** (new, recommended) | `new_properties.xml` | `%APPDATA%\sc4pimx\` |
| PIM-X (old, being phased out) | `new_properties.xml` | the PIM-X installation folder, usually `C:\Program Files (x86)\SC4PIM` |
| iLive Reader 1.5.4 | `new_properties.xml` | the Reader installation folder, usually `C:\Program Files (x86)\ILives\ILives Reader` |
| iLive Reader 0.9.3 | `tropod_Properties.xml` | the Reader installation folder, usually `C:\Program Files (x86)\ILives\ilive_reader093` |

Restart the tool after replacing the file.

## Using it with PIM-X

The generators compute the statistics when a lot is **created or rebuilt** in PIM-X: existing lots keep the values
they were made with. To give existing lots the values of a new version of this file, open them in PIM-X and use
*Rebuild Properties*, then replace the lots in your Plugins folder (and, for buildings already placed in a city, plop
them again or let them regrow).

A building made by another author with another properties file keeps that author's values, even in a game where you
use this file: the model belongs to the building, not to the game.

## Civic and utility balance model

The generators of police, education, health, water, garbage and power share a few rules, with their constants in the
Ploppable category so they can be tuned in one place. The full formulas, reference values and the reasons for every
change are in **[docs/balance-model.md](docs/balance-model.md)**.

| Rule | Formula | Anchor |
|---|---|---|
| Monthly cost | cost per resident served (`CostPerResident` = 0.125 per month) x a factor per family; within a family it grows with capacity^0.9 | The Maxis buildings of `SimCity_1.dat`, on which the game's tax income is balanced |
| Power plants | cost per MW x a factor per fuel (coal 0.6 ... microwave 1.6) | On average the Maxis cost per MW, with a 1 to 2.7 range instead of 1 to 6 |
| Plop cost | months of monthly cost: `PaybackCivic` 30, `PaybackWater` 12, `PaybackGarbage` 25, power by fuel (`PaybackFuel` 20 for gas to 80 for nuclear and hydro) | Real construction costs measured in running costs; the SC4SIM starting funds |
| Coverage radius | schools and hospitals cover the circle holding the residents they serve, at 5,000 residents per km2; fire and police stations on the Maxis scale | Maxis radii (16 m per cell) |
| Jobs | schools one per 15 students, colleges one per 20, hospitals one per 60 patients; power plants by technology (coal and nuclear the most, gas, hydro, solar and wind the fewest) | The Maxis buildings and real staffing |
| Capacity caps | elementary 2,500 students, high school 4,500, private school 1,500 | Large real schools; the Maxis Large High School |

Reference values (monthly cost / plop cost):

| Building | SC4SIM model | Maxis |
|---|---|---|
| Elementary school, 1,000 students | 800 / 24,000 | K-8 School, 500 students: 400 |
| High school, 4,500 students | 3,560 | Large High School, 4,500 students: 3,750 |
| Clinic, 500 patients | 320 | Medical Clinic, 500 patients: 400 |
| Coal plant, 19,600 MW | 1,450 | Coal, 6,000 MW: 550 |
| Nuclear plant, 16,000 MW | 2,200 | Nuclear, 16,000 MW: 3,000 |
| Solar plant, 5,000 MW | 950 | Solar, 5,000 MW: 1,000 |

The model was checked in a running city through [SC4MCP](https://github.com/UlisseWolf/SC4MCP): every SC4SIM building
costs in the game exactly what the formulas give.

## Verification

`tools/check_pimx.py` runs the PIM-X generator code itself, without its user interface:

1. it evaluates every generator category of the XML, as PIM-X *Rebuild Properties* does, and reports the categories
   that fail;
2. with `--package`, it recomputes the building exemplars of an installed SC4SIM package and lists every building whose
   capacity, plop cost, monthly cost, jobs or coverage radius differ from what the XML gives.

```sh
python tools/check_pimx.py --pimx /path/to/sc4pim-x/src --xml new_properties.xml
python tools/check_pimx.py --pimx /path/to/sc4pim-x/src --xml new_properties.xml \
    --package "Plugins/050-load-first/cam.sc4-system-integration-module.stable.4.0.2.sc4pac" \
    --files CAM_Education_Buildings.dat CAM_Health_Buildings.dat CAM_Police_Fire_Buildings.dat \
            CAM_Power_Garbage_Buildings.dat CAM_Water_Buildings.dat
```

It needs Python 3.10 or later and the [PIM-X sources](https://github.com/caspervg/sc4pim-x); wxPython is not needed.
The exit code is 0 when everything matches. The current file evaluates all 992 generators except four placeholders
that are not meant to be used (Network Enabling Dummy, Stoplight, RR Crossing, Effect), and an SC4SIM package rebuilt
with it reports no differences.

## Repository layout

| Path | Content |
|---|---|
| `new_properties.xml` | Property definitions, generators and occupant groups (PIM-X, iLive Reader 1.5.4) |
| `tropod_Properties.xml` | Property definitions for iLive Reader 0.9.3 |
| `docs/balance-model.md` | The civic and utility balance model: formulas, reference values, revision history |
| `tools/check_pimx.py` | Headless check of the generators with the PIM-X code |
| `LICENSE` | GNU Lesser General Public License 2.1 |

## Changelog

**2026-11-19 - civic and utility balance (SC4 SIM)**
- Monthly costs anchored to the Maxis buildings (cost per resident served), plop costs as months of upkeep, power
  plant costs by fuel.
- Coverage radii on the Maxis scale, then from the residents served for schools and hospitals.
- Civic and utility jobs on the Maxis and real-world scale; power plant staff by technology; pump operators.
- School capacity caps; parks priced by their effects; plop costs of fire stations and the Disease Center fixed.
- Syntax errors fixed in the Fresh Water Pump plop cost, the Treatment Plant and Biomass bulldoze costs; Cemetery,
  Crematorium and Power Storage generators repaired.
- `tools/check_pimx.py` added.

Details in [docs/balance-model.md](docs/balance-model.md). Earlier versions are tagged
[1.0.0 and 1.0.1](https://github.com/UlisseWolf/New_Properties.xml-patches/tags).

## Contributing

Issues and pull requests are welcome. For a change to a generator:

- keep the constants of the balance model in the Ploppable category rather than numbers inside single formulas;
- run `tools/check_pimx.py` and include its result in the pull request;
- describe the effect on a few real buildings (before and after) and, if the model changes, update
  `docs/balance-model.md`.

## Credits

- **Maxis** - SimCity 4 and the original property definitions.
- **NAM Team** and the **BSC Team** - the original `New_Properties.xml` this file is based on.
- **caspervg** - [PIM-X](https://github.com/caspervg/sc4pim-x), whose generator code `tools/check_pimx.py` uses.
- **iLive** - the Reader.
- The authors of CAM, SPAM, Colossus Farming, ERM and NAM-MTA, whose specifications this file follows.

## License

This repository is released under the [GNU Lesser General Public License, version 2.1](LICENSE).

You may use `new_properties.xml` and `tropod_Properties.xml` with any modding tool, and distribute lots, exemplars
and plugins made with them under any license: the license applies to these files, not to the content you create with
them. If you distribute a modified version of the files themselves, it must stay under the LGPL 2.1 and come with its
changes.

SimCity 4 is a trademark of Electronic Arts Inc. This project is not affiliated with or endorsed by Electronic Arts.
