# Validation against golden_UK_Nordics_22Oct

## Company fields (golden_values.csv)

| Company | Field | Golden | FY | Ours | Result |
|---|---|---|---|---|---|
| Shell PLC | lei | 21380068P1DRHMJ8KU70   |  | 21380068P1DRHMJ8KU70  | match |
| Shell PLC | listing_status | listed   |  | listed  | match |
| AO World PLC | lei | 2138005FFOAJIUZY4375   |  | 2138005FFOAJIUZY4375  | match |
| AO World PLC | listing_status | listed   |  | listed  | match |
| BioArctic AB | lei | 549300Y0OI2WVUNHLC33   |  | 549300Y0OI2WVUNHLC33  | match |
| Equinor ASA | lei | OW6OFBNCKXC4US5C7523   |  | OW6OFBNCKXC4US5C7523  | match |
| Aker Carbon Capture ASA | country_code | NO   |  | NO  | match |
| Aker Carbon Capture ASA | lei | 549300JXF011KX2HXT02   |  | 549300JXF011KX2HXT02  | match |
| Novo Nordisk A/S | lei | 549300DAQ1CVT6CXN342   |  | 549300DAQ1CVT6CXN342  | match |
| Novo Nordisk A/S | listing_status | listed   |  | listed  | match |
| Bang & Olufsen A/S | lei | 52990018KGR3ILFDNJ20   |  | 52990018KGR3ILFDNJ20  | match |
| Bang & Olufsen A/S | listing_status | listed   |  | listed  | match |
| Nokia Corporation | fte | 78400   | 2025 | 78005 employees | match |
| Nokia Corporation | lei | 549300A0JPRWG1KI7U06   |  | 549300A0JPRWG1KI7U06  | match |
| Nokia Corporation | revenue | 19220.0 millions EUR | 2025 | 19889000000 EUR | differs |
| Nokia Corporation | total_assets | 39149.0 millions EUR | 2025 | 37597000000 EUR | differs |
| Marimekko Oyj | lei | 74370053IOY42B9YJ350   |  | 74370053IOY42B9YJ350  | match |
| Marimekko Oyj | listing_status | listed   |  | listed  | match |

Company fields: 16 match, 2 differ, 0 missing.

## Executive pay (golden_role_pay.csv)

Each golden figure is matched to any of our role rows for the company with the same value (1% tolerance); titles don't have to agree.

| Company | Golden role | Year | Field | Golden | Ours (same field, any role) | Result |
|---|---|---|---|---|---|---|
| Volvo AB | MGMT | 2025 | comp_base_salary | 92,087,355 SEK | President and CEO=22868000; Other members of the G=92087355 | match |
| Volvo AB | MGMT | 2025 | comp_sti_actual | 29,433,500 SEK | President and CEO=9125000; Other members of the G=29433500 | match |
| Volvo AB | MGMT | 2025 | comp_lti_actual | 73,527,967 SEK | President and CEO=30687000; Other members of the G=73527967 | match |
| Volvo AB | MGMT | 2025 | pension_contribution | 28,175,941 SEK | President and CEO=7775000; Other members of the G=28175941 | match |
| Volvo AB | MGMT | 2025 | benefits_value_total | 11,164,464 SEK | President and CEO=425000; Other members of the G=11164464 | match |
| Volvo AB | MGMT | 2025 | comp_sti_target | 40 SEK |  | missing |
| Volvo AB | MGMT | 2025 | comp_sti_max | 80 SEK | President and CEO=100; Other members of the G=80 | match |
| Volvo AB | MGMT | 2025 | comp_lti_target | 40 SEK |  | missing |
| Volvo AB | MGMT | 2025 | comp_lti_max | 80 SEK | President and CEO=150; Other members of the G=80 | match |
| BioArctic AB | MGMT | 2025 | comp_base_salary | 17,549,000 SEK | CEO=4846000; Board member=2382000; Other senior executive=17549000 | match |
| BioArctic AB | MGMT | 2025 | comp_sti_actual | 7,042,000 SEK | CEO=2253000; Other senior executive=7042000 | match |
| BioArctic AB | MGMT | 2025 | comp_lti_actual | 4,647,000 SEK | CEO=1650000; CEO=10000; Other senior executive=4647000 | match |
| BioArctic AB | MGMT | 2025 | pension_contribution | 3,838,000 SEK | CEO=1629000; Board member=452000; Other senior executive=3838000 | match |
| BioArctic AB | MGMT | 2025 | comp_sti_target | 20 SEK | CEO=50; Other senior executive=40 | differs |
| BioArctic AB | MGMT | 2025 | comp_sti_max | 40 SEK | CEO=50; Other senior executive=80 | differs |
| BioArctic AB | MGMT | 2025 | comp_lti_target | 131 SEK |  | missing |
| BioArctic AB | CEO | 2025 | comp_base_salary | 4,967,000 SEK | CEO=4846000; Board member=2382000; Other senior executive=17549000 | differs |
| BioArctic AB | CEO | 2025 | comp_sti_actual | 5,276,000 SEK | CEO=2253000; Other senior executive=7042000 | differs |
| BioArctic AB | CEO | 2025 | comp_lti_actual | 1,650,000 SEK | CEO=1650000; CEO=10000; Other senior executive=4647000 | match |
| BioArctic AB | CEO | 2025 | pension_contribution | 1,629,000 SEK | CEO=1629000; Board member=452000; Other senior executive=3838000 | match |
| BioArctic AB | CEO | 2025 | comp_sti_target | 25 SEK | CEO=50; Other senior executive=40 | differs |
| BioArctic AB | CEO | 2025 | comp_sti_max | 50 SEK | CEO=50; Other senior executive=80 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_base_salary | 516,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_actual | 113,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_lti_actual | 135,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | pension_contribution | 123,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | benefits_value_total | 156,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | comp_base_salary | 373,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | comp_sti_actual | 81,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | comp_lti_actual | 92,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | pension_contribution | 96,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | benefits_value_total | 55,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Legal & Compliance (LEG) | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | comp_base_salary | 425,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | comp_sti_actual | 94,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | comp_lti_actual | 105,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | pension_contribution | 116,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | benefits_value_total | 111,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Safety, Security & Susta | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Communication (COM) | 2025 | comp_base_salary | 367,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Communication (COM) | 2025 | comp_sti_actual | 79,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Communication (COM) | 2025 | comp_lti_actual | 92,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Communication (COM) | 2025 | pension_contribution | 99,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Communication (COM) | 2025 | benefits_value_total | 47,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Communication (COM) | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Communication (COM) | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | comp_base_salary | 543,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | comp_sti_actual | 121,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | comp_lti_actual | 134,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | pension_contribution | 130,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | benefits_value_total | 70,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Marketing, Midstream & P | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | comp_base_salary | 479,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | comp_sti_actual | 101,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | comp_lti_actual | 122,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | pension_contribution | 110,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | benefits_value_total | 152,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Projects, Drilling & Pro | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | comp_base_salary | 381,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | comp_sti_actual | 83,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | comp_lti_actual | 96,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | pension_contribution | 104,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | benefits_value_total | 56,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP People & Organisation (P | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Power (PWR) | 2025 | comp_base_salary | 163,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Power (PWR) | 2025 | comp_sti_actual | 34,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Power (PWR) | 2025 | comp_lti_actual | 22,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Power (PWR) | 2025 | pension_contribution | 35,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Power (PWR) | 2025 | benefits_value_total | 39,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Power (PWR) | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Power (PWR) | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | comp_base_salary | 494,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | comp_sti_actual | 111,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | comp_lti_actual | 122,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | pension_contribution | 19,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | benefits_value_total | 64,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Technology, Digital & In | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_base_salary | 622,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_actual | 152,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_lti_actual | 152,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | pension_contribution | 144,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | benefits_value_total | 110,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP Exploration & Production | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | comp_base_salary | 266,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | comp_sti_actual | 54,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | comp_lti_actual | 69,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | pension_contribution | 65,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | benefits_value_total | 27,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | Acting EVP Renewables (REN) | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | CEO | 2025 | comp_base_salary | 1,242,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | CEO | 2025 | comp_sti_actual | 292,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | CEO | 2025 | comp_lti_actual | 306,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | CEO | 2025 | pension_contribution | 254,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | CEO | 2025 | benefits_value_total | 119,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | CEO | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | CEO | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | comp_base_salary | 579,000 USD | President and chief ex=1242000; EVP Marketing, Midstre=543000; EVP Safety, Security& =4250 | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | comp_sti_actual | 126,000 USD | President and chief ex=292000; EVP Marketing, Midstre=121000; EVP Safety, Security& =94000 | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | comp_lti_actual | 154,000 USD | President and chief ex=306000; EVP Marketing, Midstre=134000; EVP Safety, Security& =10500 | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | pension_contribution | 132,000 USD | President and chief ex=254000; EVP Marketing, Midstre=130000; EVP Safety, Security& =11600 | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | benefits_value_total | 73,000 USD | President and chief ex=119000; EVP Marketing, Midstre=70000; EVP Safety, Security& =111000 | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | comp_sti_target | 13 USD | President and chief ex=12.5; EVP Marketing, Midstre=12.5; EVP Safety, Security& =12.5; Act | match |
| Equinor ASA | EVP and Chief financial offi | 2025 | comp_sti_max | 25 USD | President and chief ex=25; EVP Marketing, Midstre=25; EVP Safety, Security& =25; Acting EV | match |
| Novo Nordisk A/S | CFO | 2025 | comp_base_salary | 10,300,000 DKK | CEO=7100000; CFO=10300000; Non-registered executi=55400000; Former CEO (until 6 Au=1130000 | match |
| Novo Nordisk A/S | CFO | 2025 | comp_sti_actual | 2,600,000 DKK | CEO=4400000; CFO=2600000; Non-registered executi=16500000; Former CEO (until 6 Au=3500000; | match |
| Novo Nordisk A/S | CFO | 2025 | comp_lti_actual | 8,700,000 DKK | CEO=6500000; CFO=4500000; Non-registered executi=22500000; Former CEO (until 6 Au=6100000; | differs |
| Novo Nordisk A/S | CFO | 2025 | pension_contribution | 1,000,000 DKK | CEO=700000; CFO=1000000; Non-registered executi=7800000; Former CEO (until 6 Au=1100000; F | match |
| Novo Nordisk A/S | CFO | 2025 | benefits_value_total | 300,000 DKK | CEO=2000000; CFO=300000; Non-registered executi=7700000; Former CEO (until 6 Au=200000; Fo | match |
| Novo Nordisk A/S | CFO | 2025 | comp_sti_target | 50 DKK |  | missing |
| Novo Nordisk A/S | CFO | 2025 | comp_sti_max | 100 DKK | CEO=100; CFO=100; Non-registered executi=100; Former CEO (until 6 Au=100; Former non-regis | match |
| Novo Nordisk A/S | CFO | 2025 | comp_lti_target | 100 DKK |  | missing |
| Novo Nordisk A/S | CFO | 2025 | comp_lti_max | 200 DKK | CEO=250; CFO=200; Non-registered executi=200; Former CEO (until 6 Au=250; Former non-regis | match |
| Novo Nordisk A/S | CEO | 2025 | comp_base_salary | 7,100,000 DKK | CEO=7100000; CFO=10300000; Non-registered executi=55400000; Former CEO (until 6 Au=1130000 | match |
| Novo Nordisk A/S | CEO | 2025 | comp_sti_actual | 4,400,000 DKK | CEO=4400000; CFO=2600000; Non-registered executi=16500000; Former CEO (until 6 Au=3500000; | match |
| Novo Nordisk A/S | CEO | 2025 | comp_lti_actual | 9,100,000 DKK | CEO=6500000; CFO=4500000; Non-registered executi=22500000; Former CEO (until 6 Au=6100000; | differs |
| Novo Nordisk A/S | CEO | 2025 | pension_contribution | 700,000 DKK | CEO=700000; CFO=1000000; Non-registered executi=7800000; Former CEO (until 6 Au=1100000; F | match |
| Novo Nordisk A/S | CEO | 2025 | benefits_value_total | 2,000,000 DKK | CEO=2000000; CFO=300000; Non-registered executi=7700000; Former CEO (until 6 Au=200000; Fo | match |
| Novo Nordisk A/S | CEO | 2025 | comp_sti_target | 50 DKK |  | missing |
| Novo Nordisk A/S | CEO | 2025 | comp_sti_max | 100 DKK | CEO=100; CFO=100; Non-registered executi=100; Former CEO (until 6 Au=100; Former non-regis | match |
| Novo Nordisk A/S | CEO | 2025 | comp_lti_target | 125 DKK |  | missing |
| Novo Nordisk A/S | CEO | 2025 | comp_lti_max | 250 DKK | CEO=250; CFO=200; Non-registered executi=200; Former CEO (until 6 Au=250; Former non-regis | match |
| Bang & Olufsen A/S | CEO | 2025 | comp_base_salary | 6,973,000 DKK | Executive Vice Preside=4137000; Chief Executive Office=5345000; Executive Vice Preside=307 | differs |
| Bang & Olufsen A/S | CEO | 2025 | comp_sti_actual | 10,723,000 DKK | Executive Vice Preside=5008000; Chief Executive Office=12844000; Executive Vice Preside=37 | differs |
| Bang & Olufsen A/S | CEO | 2025 | comp_lti_actual | 7,079,000 DKK | Executive Vice Preside=114046; Executive Vice Preside=3786000; Chief Executive Office=2919 | differs |
| Bang & Olufsen A/S | CEO | 2025 | benefits_value_total | 907,000 DKK | Executive Vice Preside=1520000; Chief Executive Office=702000; Executive Vice Preside=3150 | differs |
| Bang & Olufsen A/S | CEO | 2025 | comp_sti_target | 50 DKK | Executive Vice Preside=50; Chief Executive Office=100; Executive Vice Preside=50 | match |
| Bang & Olufsen A/S | CEO | 2025 | comp_sti_max | 100 DKK | Executive Vice Preside=43.75; Chief Executive Office=175; Executive Vice Preside=43.75 | differs |
| Bang & Olufsen A/S | CEO | 2025 | comp_lti_target | 75 DKK |  | missing |
| Bang & Olufsen A/S | CEO | 2025 | comp_lti_max | 150 DKK | Executive Vice Preside=125; Chief Executive Office=150; Executive Vice Preside=125 | match |
| Bang & Olufsen A/S | CFO | 2025 | comp_base_salary | 3,595,000 DKK | Executive Vice Preside=4137000; Chief Executive Office=5345000; Executive Vice Preside=307 | differs |
| Bang & Olufsen A/S | CFO | 2025 | comp_sti_actual | 4,426,000 DKK | Executive Vice Preside=5008000; Chief Executive Office=12844000; Executive Vice Preside=37 | differs |
| Bang & Olufsen A/S | CFO | 2025 | comp_lti_actual | 2,966,000 DKK | Executive Vice Preside=114046; Executive Vice Preside=3786000; Chief Executive Office=2919 | differs |
| Bang & Olufsen A/S | CFO | 2025 | pension_contribution | 431,000 DKK | Executive Vice Preside=496000; Executive Vice Preside=369000; Executive Management B=10000 | differs |
| Bang & Olufsen A/S | CFO | 2025 | benefits_value_total | 165,000 DKK | Executive Vice Preside=1520000; Chief Executive Office=702000; Executive Vice Preside=3150 | differs |
| Bang & Olufsen A/S | CFO | 2025 | comp_sti_target | 23 DKK | Executive Vice Preside=50; Chief Executive Office=100; Executive Vice Preside=50 | differs |
| Bang & Olufsen A/S | CFO | 2025 | comp_sti_max | 46 DKK | Executive Vice Preside=43.75; Chief Executive Office=175; Executive Vice Preside=43.75 | differs |
| Bang & Olufsen A/S | CFO | 2025 | comp_lti_target | 63 DKK |  | missing |
| Bang & Olufsen A/S | CFO | 2025 | comp_lti_max | 125 DKK | Executive Vice Preside=125; Chief Executive Office=150; Executive Vice Preside=125 | match |

Pay figures: 120 match, 19 differ, 9 missing (of 148).

