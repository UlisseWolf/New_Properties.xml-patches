# New_Properties.xml-patches
New_Properties.xml is the file that contains all the prorpeity definitions used in the exemplar and cohort files of SimCity 4. The file contains the algorithms for generating the statistics for the various lots

## Features

New_Properties.xml is an XML file that is used by the modding tools of PIM-X and ILives Reader in reading all propieties of SimCity 4 exemplars.  For this reason this file is essential in reading and creating the exemplar files

The file contains all the algorithms used to calculate building statistics (Residential, Commercial, Industrial, Civic and Utility) as well as generate TE (Transit Enable) switches and calculate station capacity. 

The file contains all the Occupant Groups that Maxis and BSC Team have developed allowing for better lot management. 

Because of the uniqueness of the file, new properties can be generated that the game can read using Mod DLLs and it also allows the identification of the IIDs of the prorpieties that can be used for any LUA codes to be used in the game.

## Advanced Features

Unlike the original [New_Properrty.xml](https://github.com/NAMTeam/New_Properties.xml) file, this version contains the following differences

- Public services (education, public safety, healthcare) have been completely overhauled, with a capacity increase four times that of the BSC version and twice that of the Maxis version, since the BSC version has values equal to half those of the Maxis version, forcing the player to build more civic buildings.
- No delays in the release of patches and new buildings compared to the original New_Property.xml

Except for these two differences, the two versions have the same patches, additional buildings, and additional properties created by the DLL Mods

Below are all the changes included in this version

- Public services (education, public safety, healthcare) have been completely overhauled, with a capacity increase four times that of the BSC version and twice that of the Maxis version, since the BSC version has values equal to half those of the Maxis version, forcing the player to build more civic buildings
- The educational buildings are compatible with the Education Realism Mod (ERM) and specific CAM, and they also add new buildings such as a kindergarten and a modular university.
- The utilities have been revised to include new types of power plants, electrical substations, and batteries, as well as to re-enable features removed by Maxis, such as the Freshwater Pump, Desalination Plant, and Incinerator.
- Transit-Enabled (TE) buildings comply with NAM-MTA specifications
- All additional properties created by the DLL Mods have been added
- Update all Occupant Groups (OG) by adding the recovered ones and the new ones
- Added Farm Files from SPAM and Colossus Farming, in addition to updating the BSC ones
- The park system has been revised and improved compared to the BSC & Maxis version
- Added additional buildings from the CAM expansions
- Additional buildings and properties from the CAM expansions have been added
- Ability to generate farms up to Stage 10 (Requires CAM or SPAM for Stages 4 and 5—Requires CAM for Stages 5 through 10)
- SC4SIM deathcare (SC4SIM.dll 1.9.4 or later): the properties SC4SIM Deathcare Type, Capacity and Radius (0x5C4DD001-0x5C4DD003), the occupant groups Crematorium (0x5C4DD100) and Cemetery (SC4SIM Deathcare, 0x5C4DD101), the Cemeteries (0x5C4DD200) and Crematoria (0x5C4DD201) submenus under Health and two generators under Hospital: Cemetery (SC4SIM Deathcare) and Crematorium (SC4SIM Deathcare). The Reward Cemetery generator is unchanged
- LotConfigPropertyZoneTypes: zone 0x0D is shown as I - Manufacturing (SC4SIM ManufacturingZone) instead of Spaceport
- Mixed-Use (R-C-I) growables: a new category under R-C-I, grouped like the R-C-I growables. Mixed-Use Residential: homes above shops (R/CS $, $$, $$$), Live-Work (R/I-m $$) and Farmstead (R/I-a $). Mixed-Use Commercial: shops with apartments (CS/R $, $$, $$$) and offices with apartments (CO/R $$, $$$). Mixed-Use Industrial: Farm with Farmhouse (I-a/R $), Farm with Farmhouse and Farm Shop (I-a/R/CS $), Workshop with Flats (I-m/R $$) and Tech Campus (I-ht/R $$$). Each one also W2W. They need SC4SIM.dll (MixedOccupancy): every generator sets Allow Joint Occupancy = true and gives the secondary uses the building's own wealth, the only wealth the game fills. Their query exemplars point to the mixed-use queries of the CAM's CAM_UI.dat (0x5C4DE200-0x5C4DE20B), which add rows with the occupancy and capacity of the secondary uses (SC4QueryUIHooks.dll) Occupant groups, as for the R-C-I growables: Building: Mixed-Use (R-C-I) (0x5C4DE000, every mixed-use building), Mixed-Use Residential, Commercial and Industrial (0x5C4DE010, 0x5C4DE020, 0x5C4DE030, by group) and one per generator (0x5C4DE011-0x5C4DE015, 0x5C4DE021-0x5C4DE025, 0x5C4DE031-0x5C4DE034), next to the usual R, C and I occupant groups of each use

- Civic and utility balance for the SC4 SIM (police, education, health, water, garbage, power): monthly costs follow one cost per resident served and plop costs are months of monthly cost, sized for the SIM starting funds. See [Civic and utility balance](#civic-and-utility-balance-sc4-sim) below

This version of New_property.xml is the version that always contains the latest changes available compared to the original version, which will have delayed updates (New Building & Patches).

We strongly recommend choosing the right version for your modding project. As a general rule, 

- New_Property.xml -> Recommended for a vanilla or hybrid vanilla experience
- New_Properties.xml-patches -> Recommended for a CAM experience (CAM, CAM-SPAM, and CAM-Vanilla) or a hybrid experience

## Installation

The file must be installed by following precise instructions according to the program it is to read

### OLD PIM-X (Note: The old PIM-X is being phased out. We recommend using the new PIM-X.)

New_Properties.xml should be installed in the PIM-X installation folder (generally the installation folder is this)`C:\Program Files (x86)\SC4PIM` replacing the original file. 

### NEW PIM-X

New_Properties.xml must be installed in the following folder `%APPDATA%\sc4pimx\`

### Ilives - Reader (1.5.4)

New_Properties.xml should be installed in the Reader installation folder `C:\Program Files (x86)\ILives\ILives Reader` replacing the original file. 

### Ilives - Reader (0.9.3)

This version of Reader does not use New_Properties.xml but tropod_Properties.xml. tropod_Properties.xml should be installed in the Reader installation folder (generally the installation folder is this) `C:\Program Files (x86)\ILives\ilive_reader093` replacing the original file. 

## Civic and utility balance (SC4 SIM)

The generators of police, education, health, water, garbage and power share three rules (constants in the Ploppable category, so they can be tuned in one place):

- **Monthly cost = cost per resident served, at the Maxis level.** `CostPerResident` = 0.125 per month, anchored to the Maxis buildings of `SimCity_1.dat`, on which the game's tax income is balanced: with it the K-12 schools cost what the Maxis schools cost per student (K-8 School 500 students for 400 a month, Larger Elementary 3,000 for 2,000, 9-12 School 750 for 750, Large High School 4,500 for 3,750). Each family is scaled to the cost per unit of its Maxis buildings: health 3.5 (Maxis clinic 500 patients for 400, medical center 3,000 for 1,200), K-12 5.0 per student (high school 1.2 and private school 1.8 times the elementary cost per student), libraries 0.035 (Maxis small library 30,000 for 250; the SC4SIM Main City Library 480,000 for 2,150), museums 1.0 by capacity (the SC4SIM Science Museum, 2,800 visitors, costs 450 like the Maxis museum), power `PowerCostPerMW` = 1.0 x `CostPerResident`, water 0.2 (an aquifer pump costs 0.026 per unit, Maxis pumps 0.016-0.021), recycling 0.1. Police already cost what the Maxis precincts cost (4-car 125, 36-car 250) and keep their formula; fire stations are unchanged. Capacities stay the SIM ones, so one SIM building replaces several Maxis ones and costs about as much as they would together. Inside a family the cost grows with capacity^0.9, so larger buildings are slightly cheaper per unit.
- **Power plants cost per MW by fuel** (`FuelFactor` x `PowerCostPerMW` = 0.125): coal 0.6, oil 0.75, hydroelectric 0.8, natural gas and biomass 0.9, geothermal and waste to energy 1.0, nuclear fission 1.1, electric generator and auxiliary 1.2, nuclear fusion/hydrogen 1.25, tidal 1.4, solar and wind 1.5, microwave 1.6. On average this is the Maxis cost per MW (coal 0.042, oil 0.086, gas 0.13, nuclear 0.19, solar 0.20); dirty power stays cheapest, but the range is 1 to 2.7 instead of 1 to 6. Water: desalination 2.5 and fresh water pumps 0.8 times the aquifer cost per unit.
- **Plop cost = months of monthly cost**, because the SIM starting funds (1,000,000 / 750,000 / 500,000) are 10-25 times the Maxis ones: `PaybackCivic` 30 (close to the 35 months a real school costs to build, measured in its running costs), `PaybackPower` 50, `PaybackWater` 12 (water works serve very large populations: the 1,605,000-unit SC4SIM desalination plant costs 811,200 instead of 2.7 million), `PaybackGarbage` 25.

Reference values with these formulas (monthly / plop): elementary school 1,000 students 800 / 24,000; elementary 3,000 students 2,050 (Maxis Larger Elementary 2,000); high school 1,000 students 937 / 28,150; high school 4,500 students 3,560 (Maxis Large High School 3,750); clinic 500 patients 320 (Maxis 400); clinic 2,600 patients 1,390 / 41,700; small library 40,000 250; science museum 2,800 450 (Maxis museum 450); coal 19,600 MW 1,450 / 72,500; nuclear 16,000 MW 2,200 (Maxis 3,000); gas 3,000 MW 350 (Maxis 400); solar 5,000 MW 950 (Maxis 1,000); aquifer pump 91,000 2,050 / 24,500.

**Revision (2026-11-19).** The first version anchored `CostPerResident` at 0.032 on an estimate of the tax income (0.20 per resident per month) and gave health 1.0, libraries 0.1 and power 2.0: monthly costs came out 4 to 12 times below the Maxis buildings per unit served (a 2,600-patient clinic cost 110 a month, a 1,000-student school 200). The anchor is now the Maxis buildings themselves, read from `SimCity_1.dat`.

**Verification with PIM-X (2026-11-19).** The formulas were recomputed with the PIM-X code itself (its category reader and its Rebuild Properties routine, `build_category_props_for_preset`), on every generator category and on the SC4SIM building exemplars with their lots. Fixed on the way:

- *Cemetery* and *Crematorium (SC4SIM Deathcare)* could not be rebuilt: the Hospital parent evaluates the hospital radius and patients (`Radius`, `Patients`) before the category removes them, and they were not defined. They are now defined (0) and the plop cost is `PaybackCivic` months of the monthly cost (50 / 1,500 and 120 / 3,600 for a 4x4 lot) instead of the hospital formula from volume.
- *Power Storage*: Power Consumed used `PopulationServed`, copied from the incinerator and not defined there; it now uses the default `BiasedBC` formula.
- *Stadium* inherited the new park cost, so the reward stadiums came out at half their monthly cost; the stadiums keep the former formulas, as Neutral Park and Watercrafts.
- Museums and the Main City Library came out at 4 and 2 times their former cost: factors 1.0 and 0.035 (see above).
- Water plop costs with `PaybackWater` 40 reached 2.7 million for the desalination plant: now 12.

All 992 generator evaluations now succeed except the four placeholders that are not meant to be used (Network Enabling Dummy, Stoplight, RR Crossing, Effect). PIM-X expands the `eval` variables by plain text replacement; a comparison with a token-based expansion found no variable name that corrupts another. Parks: rebuilt with PIM-X, the hand-tuned SIM Greens 1-3 give 5 / 10 / 20 (their effects come from the lot size, 1x1).

Unchanged: capacities, radii and outputs, the College and Opera monthly costs, the Jail, and the reward buildings (Disease Center, Farmers Market, Prison, Toxic Dump), the SC4SIM deathcare buildings and fire stations. Fixed on the way: syntax errors in the Fresh Water Pump plop cost, the Treatment Plant bulldoze cost and the Biomass bulldoze cost.

The SIM exemplars must be regenerated with PIM-X to take the new values.

**Parks.** A park now costs what it gives: monthly cost = park effect (magnitude x radius / 45) + landmark effect (magnitude x radius / 90) + cap relief per wealth / 2000, at least 5, in steps of 5; plop cost = `PaybackCivic` (30) months. The former formula (inherited from the BSC/NAM file) added a fixed 5 + int(50 + Worth/10), so every 1x1 park cost about 60-70 per month whatever its effect, and a large park cost less per cell than a small one. Neutral Park and Watercrafts keep the former formulas (about 64 per month, plop 0). Effects, radii and cap relief are unchanged (the unused `ParkEffectConst` stays unused, as in the NAM file). Examples, old -> new monthly: 1x1 park 69 -> 5, 4x4 park 144 -> 35, 4x4 playground 144 -> 60, 4x4 community garden 144 -> 125, 8x8 sports court 704 -> 275. SIM parks whose exemplars were tuned by hand (Greens 1-3: 5 / 20 / 45) come out at 5 / 10 / 20 when rebuilt with PIM-X, because their effects are recomputed from the lot size; the reward stadiums keep the former formulas.
