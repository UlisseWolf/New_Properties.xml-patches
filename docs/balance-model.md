<!-- Technical reference of the balance model of new_properties.xml. Summary in README.md. -->
# Civic and utility balance model (SC4 SIM)

This page is the technical reference of the civic and utility balance of `new_properties.xml`: the formulas, the
reference values and the history of every revision, with the reasons behind each change. The [README](../README.md)
has a summary.

## Rules

The generators of police, education, health, water, garbage and power share three rules (constants in the Ploppable category, so they can be tuned in one place):

- **Monthly cost = cost per resident served, at the Maxis level.** `CostPerResident` = 0.125 per month, anchored to the Maxis buildings of `SimCity_1.dat`, on which the game's tax income is balanced: with it the K-12 schools cost what the Maxis schools cost per student (K-8 School 500 students for 400 a month, Larger Elementary 3,000 for 2,000, 9-12 School 750 for 750, Large High School 4,500 for 3,750). Each family is scaled to the cost per unit of its Maxis buildings: health 3.5 (Maxis clinic 500 patients for 400, medical center 3,000 for 1,200), K-12 5.0 per student (high school 1.2 and private school 1.8 times the elementary cost per student), libraries 0.035 (Maxis small library 30,000 for 250; the SC4SIM Main City Library 480,000 for 2,150), museums 1.0 by capacity (the SC4SIM Science Museum, 2,800 visitors, costs 450 like the Maxis museum), power `PowerCostPerMW` = 1.0 x `CostPerResident`, water 0.2 (an aquifer pump costs 0.026 per unit, Maxis pumps 0.016-0.021), recycling 0.1. Police already cost what the Maxis precincts cost (4-car 125, 36-car 250) and keep their formula; fire stations keep their monthly cost formula (2-engine 90, 4-engine 190, deluxe 240). Capacities stay the SIM ones, so one SIM building replaces several Maxis ones and costs about as much as they would together. Inside a family the cost grows with capacity^0.9, so larger buildings are slightly cheaper per unit.
- **Power plants cost per MW by fuel** (`FuelFactor` x `PowerCostPerMW` = 0.125): coal 0.6, oil 0.75, hydroelectric 0.8, natural gas and biomass 0.9, geothermal and waste to energy 1.0, nuclear fission 1.1, electric generator and auxiliary 1.2, nuclear fusion/hydrogen 1.25, tidal 1.4, solar and wind 1.5, microwave 1.6. On average this is the Maxis cost per MW (coal 0.042, oil 0.086, gas 0.13, nuclear 0.19, solar 0.20); dirty power stays cheapest, but the range is 1 to 2.7 instead of 1 to 6. Water: desalination 2.5 and fresh water pumps 0.8 times the aquifer cost per unit.
- **Plop cost = months of monthly cost**, because the SIM starting funds (1,000,000 / 750,000 / 500,000) are 10-25 times the Maxis ones: `PaybackCivic` 30 (close to the 35 months a real school costs to build, measured in its running costs), `PaybackPower` 50 (now one value per fuel, `PaybackFuel` 20 to 80: see *Model revision 2*), `PaybackWater` 12 (water works serve very large populations: the 1,605,000-unit SC4SIM desalination plant costs 811,200 instead of 2.7 million), `PaybackGarbage` 25.

## Reference values

Reference values with these formulas (monthly / plop): elementary school 1,000 students 800 / 24,000; elementary 3,000 students 2,050 (Maxis Larger Elementary 2,000); high school 1,000 students 937 / 28,150; high school 4,500 students 3,560 (Maxis Large High School 3,750); clinic 500 patients 320 (Maxis 400); clinic 2,600 patients 1,390 / 41,700; small library 40,000 250; science museum 2,800 450 (Maxis museum 450); coal 19,600 MW 1,450 / 72,500; nuclear 16,000 MW 2,200 (Maxis 3,000); gas 3,000 MW 350 (Maxis 400); solar 5,000 MW 950 (Maxis 1,000); aquifer pump 91,000 2,050 / 24,500.

## Revision (2026-11-19)

 The first version anchored `CostPerResident` at 0.032 on an estimate of the tax income (0.20 per resident per month) and gave health 1.0, libraries 0.1 and power 2.0: monthly costs came out 4 to 12 times below the Maxis buildings per unit served (a 2,600-patient clinic cost 110 a month, a 1,000-student school 200). The anchor is now the Maxis buildings themselves, read from `SimCity_1.dat`.

## Verification with PIM-X (2026-11-19)

 The formulas were recomputed with the PIM-X code itself (its category reader and its Rebuild Properties routine, `build_category_props_for_preset`), on every generator category and on the SC4SIM building exemplars with their lots. Fixed on the way:

- *Cemetery* and *Crematorium (SC4SIM Deathcare)* could not be rebuilt: the Hospital parent evaluates the hospital radius and patients (`Radius`, `Patients`) before the category removes them, and they were not defined. They are now defined (0) and the plop cost is `PaybackCivic` months of the monthly cost (50 / 1,500 and 120 / 3,600 for a 4x4 lot) instead of the hospital formula from volume.
- *Power Storage*: Power Consumed used `PopulationServed`, copied from the incinerator and not defined there; it now uses the default `BiasedBC` formula.
- *Stadium* inherited the new park cost, so the reward stadiums came out at half their monthly cost; the stadiums keep the former formulas, as Neutral Park and Watercrafts.
- Museums and the Main City Library came out at 4 and 2 times their former cost: factors 1.0 and 0.035 (see above).
- Water plop costs with `PaybackWater` 40 reached 2.7 million for the desalination plant: now 12.

## In-game test (2026-11-19, SC4MCP)

 A test city was built with the SC4SIM package installed and its budget read from the game through the SC4MCP DLL. Every SC4SIM building costs in the game exactly what the package and these formulas give: K-8 School 675 + 225 a month (27,000 plop), clinic 680 + 120, water pumping station 775 (9,300), Maxis coal 550 (27,500). With 3,671 residents the city earned 0.44 per resident per month and spent more, because the starting services are sized for 6,000 to 30,000 residents; at full capacity they cost about 0.30 per resident. Two families still had the old plop formulas and were fixed:

- *Fire Station*: `10*int(8+0.065*Volume^0.7)` made a station cheaper to build than two months of upkeep (2-engine 180 for 90 a month). Plop is now `PaybackCivic` months: 2,700 / 5,700 / 7,200 for the 2-engine, 4-engine and deluxe stations.
- *Disease Center*: had no plop formula and took the Hospital one from volume (5,460, 45 months). Now `PaybackCivic` months: 3,600.

## Coverage radii (2026-11-19)

 The radii were compared with the Maxis buildings of `SimCity_1.dat` (radii are in metres, 16 m per cell; a large city is 4,096 m wide). Fire stations, police stations, hospitals and libraries covered 2 to 4 times the Maxis radius, and the largest ones a whole large map, which made safety and health cost far less than their price per resident served. They are now on the Maxis scale (installed SC4SIM buildings, before -> after):

| Family | Formula | Values |
|---|---|---|
| Fire Station | `16*int(0.5+5.6*Volume^0.2)` (was `64*int((160+3*sqrt(2*Volume))/16)`, 640 m minimum) | 2-engine 1,280 -> 384 (Maxis 384), 4-engine 2,432 -> 576 (Maxis 585), deluxe 3,008 -> 640 (Maxis 685) |
| Police Station | `16*int(0.5+3.7*Volume^0.24)` (was `64*int((160+1.5*(2*Volume)^0.55)/16)`, 640 m minimum) | kiosk 768 -> 224, 4-car 1,536 -> 448, 36-car 2,624 -> 640, deluxe 2,816 -> 656 |
| Medical Clinic, Hospital with Helicopter, Medical Center with Helicopter (superseded by *Model revision 2*) | `16*int(1+2*Patients^0.4)` (coefficient 4 before; the medical center had a 2,400 m minimum) | 500 patients 400 (Maxis clinic 384); clinic 1,400 1,168 -> 592; Large Medical Center 18,400 3,264 -> 1,632 |
| Library | `16*int(0.5+1.45*Students^0.3)` (was `40*int(1+0.75*Students^0.4)`) | small library 40,000 2,080 -> 560 (Maxis 30,000: 512); Main City Library 480,000 5,640 -> 1,168 |

Unchanged at that step (schools are revised in *Model revision 2*): schools (their radius already grows with capacity on the Maxis scale: K-8 School 1,200 students 504 m, Maxis 500 students 384 m), and the city-wide services, which are city-wide in Maxis too (museums, colleges and universities, opera, Disease Center).

## Civic jobs (2026-11-19)

 Schools, colleges and hospitals offered far fewer jobs than the Maxis buildings and than real ones: the K-12 formula `int(ceil(Students/30)/4)` gave one job per 120 students (the Maxis 9-12 School has 100 jobs for 750 students), hospitals one per 120 residents served (Maxis clinic: one per 62), and the Disease Center inherited the hospital formula and offered 1,214 jobs. Monthly costs do not depend on jobs and are unchanged; the split between $, $$ and $$$ jobs is unchanged.

| Family | Formula | Installed SC4SIM buildings, before -> after |
|---|---|---|
| Elementary, High School, Private School | `CivicJobs = int(ceil(Students/15.))`, one per 15 students | K-8 School 16 -> 87, Larger Elementary 61 -> 447, 9-12 School 47 -> 340, Large High School 121 -> 927, private schools 17 -> 100 |
| College | `int(ceil(Students/20.))` | City College 190 -> 1,116, University 570 -> 3,396 |
| Hospital (parent of clinics and medical centers) | `int(ceil(Patients/60.))`, the Maxis clinic ratio | clinic 18 -> 29, Large Medical Center 159 -> 313 |
| Disease Center | own formula `int(ceil(Patients/1500.))` | 1,214 -> 103 |
| Fire Station | `Jobs1 = 5+int(Volume/600.)` (was `/1500.`) | 2-engine 5 -> 7, 4-engine 15 -> 27, deluxe 24 -> 43 (Maxis 7 / 28 / 28) |

Unchanged: police (7-56 jobs), libraries, museums, opera, power plants (coal 60, Maxis 48), recycling.

## Utility jobs (2026-11-19)

 Power plant jobs follow the staff a real plant of each technology needs per MW (coal and nuclear the most; gas, hydro, solar and wind the fewest), instead of gas having the most jobs per MW and nuclear and fusion the fewest. `CivicJobs = int(PowerOutput/D)` with D: coal 125, nuclear fission 125 (was 350), biomass 125 (was 150), waste to energy 100, oil 150, electric generator 200 (was 60), auxiliary 200 (was 30), natural gas 200 (was 60), solar 250 (was 150), fusion 250 (was 1,000), hydroelectric 300, geothermal 300, microwave 300, wind 300, tidal 300 (were 150). Water treatment plants and sewage sanitizers: `int(Volume/600.)` (was `/150.`). Incinerators and recycling centers: one job per 750 residents served (was 1,500). Water pumps and towers keep no jobs, as in Maxis.

| Installed SC4SIM building | Before | After | Maxis |
|---|---|---|---|
| Coal 7,500 MW | 60 | 60 | 48 (6,000 MW) |
| Natural gas 5,200 MW | 85 | 26 | 48 (3,000 MW) |
| Oil 11,600 MW | 77 | 77 | 48 (7,000 MW) |
| Nuclear 43,400 MW | 123 | 346 | 48 (16,000 MW) |
| Hydrogen 92,100 MW | 92 | 368 | 48 (50,000 MW) |
| Solar 8,000 MW | 52 | 33 | 32 (5,000 MW) |
| Waste to energy 8,500 MW | 84 | 84 | 48 (5,000 MW) |
| Water treatment plant | 114 | 28 | 16 |
| Recycling center 27,500 | 20 | 38 | 18 (25,000) |

## Model revision 2 (2026-11-19)

 Compared with real figures, the Maxis buildings and the BSC Team model:

1. *Plop cost of power plants by fuel.* A single `PaybackPower` of 50 made every plant cost 50 months of upkeep to build, while in reality capital is about two thirds of the cost of coal power, at least 60% of nuclear and about a quarter of gas. Each fuel category now sets `PaybackFuel`: nuclear fission, fusion and hydroelectric 80, tidal 70, coal, solar, wind, geothermal and microwave 60, biomass and waste to energy 40, oil 30, natural gas, electric generator and auxiliary 20. Monthly costs are unchanged. Installed plants: coal 27,500 -> 33,000, gas 30,000 -> 12,000, oil 55,000 -> 33,000, nuclear 297,500 -> 476,000, hydrogen 720,000 -> 1,152,000, solar 75,000 -> 90,000, wind 5,000 -> 6,000, waste to energy 52,500 -> 42,000.
2. *Coverage radius from the residents served.* Schools and hospitals now cover the circle that holds the residents they serve at a typical SC4 density, `SvcDensity` = 5,000 residents per km2: `Radius = 16*int(0.5+1000*sqrt(SvcResidents/(pi*SvcDensity))/16)`, with `SvcResidents` = 5 x students (students are 20% of the residents) or the patients. A building no longer covers more residents than it can serve, nor fewer, and the radius is the same rule in every family. Installed: K-8 School 504 -> 624 m, 9-12 School 848 -> 1,200 m, private schools 600 -> 672 m, clinic (1,400 patients) 592 -> 304 m, Large Medical Center (18,400) 1,632 -> 1,088 m. Fire and police stations have no capacity and keep the Maxis-anchored formulas.
3. *School capacity caps.* Elementary at most 2,500 students (a large real school; the US average is about 500), high school 4,500 (the Maxis Large High School), private school 1,500. Larger Elementary 6,600 -> 2,500 students (4,149 -> 1,749 a month); 9-12 School 5,000 and Large High School 13,800 -> 4,500 (3,562 a month each). Costs and jobs follow the capacity.
4. *Jobs.* Natural gas one job per 300 MW (was 200), nuclear fission one per 100 MW (was 125), so the gap between technologies is closer to reality (installed gas 26 -> 16, nuclear 346 -> 433). Fresh water and aquifer pumps get 3 to 10 operators (`PmpStaff`; installed pumping station 3, large pumping station 10); water towers keep none.
5. *Verification.* `tools/check_pimx.py` runs the PIM-X generator code without its GUI: it evaluates every category and, with `--package`, compares the capacity, plop cost, monthly cost, jobs and radii of an installed SC4SIM package with this XML. The installed package, rebuilt with this XML, reports 992 evaluations, the 4 placeholder failures and 0 differences.

All 992 generator evaluations now succeed except the four placeholders that are not meant to be used (Network Enabling Dummy, Stoplight, RR Crossing, Effect). PIM-X expands the `eval` variables by plain text replacement; a comparison with a token-based expansion found no variable name that corrupts another. Parks: rebuilt with PIM-X, the hand-tuned SIM Greens 1-3 give 5 / 10 / 20 (their effects come from the lot size, 1x1).

Unchanged: capacities, radii and outputs, the College and Opera monthly costs, the Jail, and the reward buildings (Farmers Market, Prison, Toxic Dump) and the SC4SIM deathcare buildings. Fire stations and the Disease Center keep their monthly cost; their plop cost is now `PaybackCivic` months (see the in-game test below). Fixed on the way: syntax errors in the Fresh Water Pump plop cost, the Treatment Plant bulldoze cost and the Biomass bulldoze cost.

The SIM exemplars must be regenerated with PIM-X to take the new values.

## Parks

 A park now costs what it gives: monthly cost = park effect (magnitude x radius / 45) + landmark effect (magnitude x radius / 90) + cap relief per wealth / 2000, at least 5, in steps of 5; plop cost = `PaybackCivic` (30) months. The former formula (inherited from the BSC/NAM file) added a fixed 5 + int(50 + Worth/10), so every 1x1 park cost about 60-70 per month whatever its effect, and a large park cost less per cell than a small one. Neutral Park and Watercrafts keep the former formulas (about 64 per month, plop 0). Effects, radii and cap relief are unchanged (the unused `ParkEffectConst` stays unused, as in the NAM file). Examples, old -> new monthly: 1x1 park 69 -> 5, 4x4 park 144 -> 35, 4x4 playground 144 -> 60, 4x4 community garden 144 -> 125, 8x8 sports court 704 -> 275. SIM parks whose exemplars were tuned by hand (Greens 1-3: 5 / 20 / 45) come out at 5 / 10 / 20 when rebuilt with PIM-X, because their effects are recomputed from the lot size; the reward stadiums keep the former formulas.
