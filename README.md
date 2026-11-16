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

- **Monthly cost = cost per resident served.** `CostPerResident` = 0.032 per month, anchored to the K-12 schools (their costs are unchanged). Each family is a fraction of it: health 1.0 (patients = residents served), K-12 1.0 (students = 20% of residents; high school 1.2 and private school 1.8 times the elementary cost per student), police 0.4 (police monthly costs x1.3), power 0.5 at 0.25 MW per resident, water 0.2 at 0.25 units per resident, recycling 0.1 at 20% reduction (the incinerator and higher reductions scale with their existing factor), libraries 0.1. A fully served city then pays about 60-65% of its tax income (about 0.20 per resident per month at 9%). Inside a family the cost grows with capacity^0.9, so larger buildings are slightly cheaper per unit; museums now cost by capacity instead of volume.
- **Power plants cost per MW by fuel** (`FuelFactor` x `PowerCostPerMW` = 0.064): coal 0.6, oil 0.75, hydroelectric 0.8, natural gas and biomass 0.9, geothermal and waste to energy 1.0, nuclear fission 1.1, electric generator and auxiliary 1.2, nuclear fusion/hydrogen 1.25, tidal 1.4, solar and wind 1.5, microwave 1.6. Dirty power stays cheapest, but the range is 1 to 2.7 instead of 1 to 5. Water: desalination 2.5 and fresh water pumps 0.8 times the aquifer cost per unit.
- **Plop cost = months of monthly cost**, because the SIM starting funds (1,000,000 / 750,000 / 500,000) are 10-25 times the Maxis ones: `PaybackCivic` 60, `PaybackPower` 100, `PaybackWater` 40, `PaybackGarbage` 100. The first services of a 25,000-resident city (police station, two schools, two clinics, a coal plant, a water pump, recycling) cost about 130,000-180,000, a fifth of the medium funds, instead of about 30,000.

Unchanged: capacities, radii and outputs, the College and Opera monthly costs, the Jail, and the reward buildings (Disease Center, Farmers Market, Prison, Toxic Dump), the SC4SIM deathcare buildings and fire stations. Fixed on the way: syntax errors in the Fresh Water Pump plop cost, the Treatment Plant bulldoze cost and the Biomass bulldoze cost.

With these formulas, the SIM buildings (exemplar values -> new values, monthly / plop): Police 4-car 90/170 -> 110/6,600; Larger Elementary 1,000/2,665 -> 1,100/66,000; Large High School 2,530/29,679 -> 2,531/151,900; Private School 1,500/3,620 -> 562/33,750; Urgent Care Clinic 700/95 -> 60/3,600; Large Medical Center 6,100/9,650 -> 630/37,800; Coal 300/13,000 -> 300/30,000; Nuclear 6,400/108,500 -> 3,050/305,000; Solar 1,600/48,000 -> 750/75,000; Water Pumping Station 500/2,150 -> 800/31,750; Recycling Center 350/5,000 -> 100/10,000. The SIM exemplars must be regenerated with PIM-X to take the new values.

**Parks.** A park now costs what it gives: monthly cost = park effect (magnitude x radius / 45) + landmark effect (magnitude x radius / 90) + cap relief per wealth / 2000, at least 5, in steps of 5; plop cost = `PaybackCivic` (60) months. The former formula (inherited from the BSC/NAM file) added a fixed 5 + int(50 + Worth/10), so every 1x1 park cost about 60-70 per month whatever its effect, and a large park cost less per cell than a small one. Neutral Park and Watercrafts keep the former formulas (about 64 per month, plop 0). Effects, radii and cap relief are unchanged (the unused `ParkEffectConst` stays unused, as in the NAM file). Examples, old -> new monthly: 1x1 park 69 -> 5, 4x4 park 144 -> 35, 4x4 playground 144 -> 60, 4x4 community garden 144 -> 125, 8x8 sports court 704 -> 275. SIM parks whose exemplars were tuned by hand (Greens 1-3: 5 / 20 / 45) come out at 5 / 25 / 50 with the same rule; the reward stadiums are not affected.
