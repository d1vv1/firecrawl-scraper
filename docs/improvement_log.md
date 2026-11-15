# What we changed before the Wave 1 run

*A plain-language tour, 3–6 November 2026.*

*Later changes are in the **Improvement log** at the bottom, one dated section per day.*

## First, what does this tool do?

Big companies publish thick reports every year: an **annual report** (how the company did:
money in, money spent, who owns it, how many people work there) and a **remuneration report**
(how much the bosses got paid). Our tool reads those reports for a long list of companies
and fills in a spreadsheet: revenue, number of employees, who the owners are, the CEO's
salary and bonus, and about 80 other facts.

For every fact it writes down **where it found it**: the page and the exact sentence. That
way a person can check any number in seconds.

It gets its facts from three kinds of places:

- **Free official databases** (like a phone book for companies): company IDs, which stock
  exchange a company is on, its country.
- **The reports themselves**, read by an AI (Google's Gemini).
- **Firecrawl**, a paid service that searches company websites when we can't find the report
  any other way. It costs "credits", which is why we try the free routes first.

Below is everything we fixed or added before running the tool on the Wave 1 list. Each item
says what was wrong, what we did, and why it matters.

---

## 1. Getting the right facts out of the reports

### The "head office" industry problem (issue 7)
**What was wrong:** for a company's industry, we used the code the government register gives
it. But for big groups that code often just says "head office". That's like asking "what
does Shell do?" and getting "it has an office". True, but useless.

**What we did:** the client already decides the industry from the company's own description
of its business, so we do the same. The AI reads the description ("we explore for and
produce oil and gas") and picks the matching code from the official EU list of 615 industries.

**Result:** 9 of 10 test companies got a real industry, against 4 before (and 3 of those 4 said "head office").

### The holding company problem (issue 6)
**What was wrong:** some UK companies are just an empty shell on top of the real business,
like a box with the actual company inside. Their own accounts showed no sales and 0
employees, because everything sits in the box underneath.

**What we did:** in that case we use the accounts of the whole group, which the company
files too. Those were often paper scans (photos of pages, no text), so we taught the tool
to read scanned pages: the AI looks at each page image and copies the text out.

**Result:** TWMA Group went from having almost nothing to having its sales, assets, profit,
592 staff, sales by country and its owner.

### Reading converted reports properly (issue 14)
Many annual reports are filed as web pages that are really a PDF drawn on screen. Our
converter turned three of six of them into garbage in two ways:

- **Table rows glued together.** "3,133" and "Directors" became "3,133Directors", so the
  staff table read as one long jumbled line. Like copying a spreadsheet into a text message
  and losing all the line breaks. We now use where each piece of text sits on the page:
  things at the same height are one row, and a new height starts a new row.
- **Letters going missing.** Some fonts draw "fi", "fl" and "ff" as one special symbol
  (fancy printing called ligatures). Our converter dropped those symbols, so "financial"
  came out as "nancial" and "profit" as "prot". One report (Bang & Olufsen) went further:
  its whole text was in a scrambled font where every letter was shifted, like a secret
  code. We now crack both. The trick is that each report also spells the same words
  normally somewhere else, so the tool works out which decoding turns the strange text into
  words that already appear in that report.

**Result:** AO World now has its staff number, and Bang & Olufsen's management pay table and
business description became readable.

### Stock market size groups (issue 9)
Nordic exchanges sort companies into Large Cap, Mid Cap and Small Cap. Before, we copied
whatever words a report used ("Large Cap Stockholm", "Nordic Main Market"). Now we ask the
stock exchange (Nasdaq) directly, using its own lists. The answer is official and the same
format for everyone.

### Company size bands in euros
The client wants each company put into a size band (large, mid, small) based on its stock
market value, measured in euros. Companies that report in pounds, kronor or kroner were
left blank because we had no exchange rate. Now we fetch the official rate from the
European Central Bank for the right day. 6 more test companies got a band.

### Dates on facts that don't change every day
Facts like "pension type" or "who owns the company" were missing a date, so the dashboard
called them incomplete. Now they get the date they belong to: the pay year, the report's
year end, or the day we read the web page (and the note says which).

---

## 2. Checking our own work

### Automatic checks on every value (issue 12)
A page the client had made scored our output, but it was just a page of results, with no
program behind it. We turned its checks into code that runs after every run. Does the
number appear in the quoted sentence? Is the quote really on that page of the report? Do
the bosses' pay parts add up to the stated total? Is the currency a real currency? And
about 20 more.

Each value gets a status: **Pass**, **Review**, **Fail**, or **Fail (hard)** (a serious
problem, like a quote that isn't in the report).

### Smarter quote matching
Many quotes were marked "not found" even though they were real. The report just printed
them in an awkward shape:

- a name split across table cells ("Executive V | ice President");
- a number written with a space instead of a comma ("22 868" for 22,868), the Swedish way;
- a row where the AI skipped some columns ("John Roberts FY26 461,262" from a longer row);
- a quote that leaves words out with "...".

We taught the matcher all of these, but strictly: the pieces must really be there, in order,
close together, and a wrong number still fails.

**Result on the 10 test companies:** serious failures went from 32 to 19, and "Pass" went
from 94% to 96%.

### Not counting "doesn't apply" as "missing"
Some boxes can never be filled. "How many people does this row cover?" makes no sense for a
single person, and a US filing number makes no sense for a company that isn't in the US. These
were counted as missing, which made us look worse than we are. Now they count as "not
applicable" and are left out of the score.

**Result:** the "found" score went from 67% to 75% without finding a single new fact, just by
counting fairly.

---

## 3. Decisions we made (issues 10 and 11)

The client's "golden" answer file has some mistakes and some odd habits. We decided not to
treat it as the truth: they collected it the same way we do, with their own errors. So:

- **Always use the newest report.** Some golden values were from the year before (issue 11).
  That's their mistake, not ours.
- **Base salary means the fixed salary only**, not salary plus perks (perks have their own box).
- **Revenue means the official IFRS revenue line.**
- **A bonus target the report doesn't state stays empty.** The golden file always made the
  target exactly half the maximum. We tried copying that rule, and it raised our score
  against their file. But it isn't true for every company: Bang & Olufsen's target is 57%,
  not 50%. So we removed it. A made-up number that looks real is worse than an honest blank.
- **Size bands use the Nasdaq Nordic limits:** €1 billion for large, €150 million for mid.

---

## 4. The dashboard

A colleague (Rahul) built a website-style dashboard to see the results: charts, filters, a
page per company, and a page per check. It had its own separate copy of the checking rules.
Two sets of rules would give two different scores, and nobody would know which was right. So:

- **The dashboard now shows our checks' results.** We removed its own rule engine.
- **It updates by itself at the end of every run.**
- **It compares each run with the one before** ("+1.2 points vs previous run").
- **Small fixes:**
  - it accepts the UK written as "UK" or "GB";
  - it showed 76% where the true number was 75.48%, because it rounded twice; now it rounds once.

---

## 5. New things the tool can do

### Pay data from a single PDF
A small extra command: give it one PDF (a remuneration report) and it pulls out only the
bosses' pay, without searching anything. Handy when you already have the file.

### Start from a pile of report files
If you only have report files and no list of companies, the tool now works out whose report
each file is:

1. **It looks for ID numbers in the text first.** Every company has unique ID numbers (like a
   passport number), and the last digits are a built-in check, so typos are caught. It checks
   each one in the global company register.
2. **If there are none, the AI reads the cover page** for the company's name and country.
3. **It works out if the file is an annual report or a pay report.** Anything else (a meeting
   agenda, say) is set aside.
4. **Then it collects all the facts** from that exact file, without searching the web, so it
   costs no credits.

We tested it on 6 real reports with their names hidden. All 6 companies were recognised
correctly, and the 3 that weren't annual or pay reports were correctly set aside.

### Reading files from your own computer
Anywhere the tool used to need a web link, it now also accepts a file on your computer.

---

## 6. Bugs we found and fixed along the way

- **A check that deleted a file.** While building the report-file feature, a check (a
  yes/no question) accidentally deleted a saved result. It now never deletes anything.
- **A missing year end.** When the report step didn't give a year end, many facts went
  undated. Now the year end printed in the report is used instead.
- **Two crashes found while running Wave 1 itself:**
  - one company's website is blocked by Firecrawl, and that stopped the whole company;
  - a date written as words ("June 2008") broke the checks.

  Both are fixed: the run carries on instead of stopping.

---

## 7. How we ran Wave 1

- **The list:** 197 companies, mostly UK and Swiss, split into two equal halves (same mix of
  countries) so two people could run them at the same time.
- **Links we couldn't use:** the Google Drive links in the list need a login, so the tool
  couldn't open them, and it searched for those reports itself.
- **Credits:** each half was capped at 550 Firecrawl credits, so together they couldn't
  overspend.
- **Half 1 result:** all 99 companies done, 5,050 facts filled, 83% passing all checks. That's
  lower than the 96% on our 10 test companies, because these UK and Swiss companies are new to
  the tool, so their hard failures are the next thing to look at.

---

# Improvement log

Each improvement is three lines:

- **Before:** what went wrong.
- **Now:** what the tool does instead.
- **Example:** a real company it helped.

---

## 11 November 2026

### Finding the right report

#### 1. A report link we give it is now really used
- **Before:** a report link in the input list was only used for bosses' pay. Revenue and the year were still searched for, and the search could fail.
- **Now:** if the search finds nothing, or only an old report, the tool reads the given link as the main report.
- **Example:** Tallink now has its 2025 year, revenue (€765m) and dated pay. 18 more companies had the same problem.

#### 2. If the search fails, look on the company's own website
- **Before:** a failed search meant no report, even when the company's website had it.
- **Now:** the tool looks through the site's own files for "Annual report 2025". It only accepts a long document with the right year on its cover.
- **Example:** Alpine Select got its 2025 report this way.

#### 3. The report must belong to the company
- **Before:** a report found on a website was used even if it was a parent company's.
- **Now:** if the name or country inside the report doesn't match, it is not used.
- **Example:** Jinhui Shipping's website holds its Hong Kong parent's report. It was used once (wrong revenue), and is now refused.

#### 4. A database search link gives the company's ID
- **Before:** some input links pointed to a database search page, not a report, so nothing was read.
- **Now:** the tool takes the company's ID number from the link and finds the official report itself.
- **Example:** K2A and SED Energy now read their official 2025 reports.

#### 5. The year is kept even when no money figures are read
- **Before:** the report's year was only saved if revenue was also read. A company with no revenue lost its year.
- **Now:** the year is always saved. If the report doesn't say it directly, it is taken from the year-end date or the cover title.
- **Example:** Chesterfield, Cobra and Commerzbank now show 2025.

### Running only what you need

#### 6. Run only some fields
- **Before:** every run collected all ~80 facts for each company, even to fix just one.
- **Now:** you can ask for just one field or a group (for example, only pay). Only those are updated; everything else stays as it was.
- **Example:** `--fields headcount` re-runs only the companies whose headcount is missing.

#### 7. The "Run required" column is followed
- **Before:** "Pay Data" or "Company Data" in the input list was ignored.
- **Now:** "Pay Data" collects only pay, "Company Data" only company facts, saving time and credits.
- **Example:** Endeavour Mining (Pay Data) had only its pay redone.

#### 8. A preview before spending credits
- **Before:** you couldn't see the cost of a run until it was over.
- **Now:** `--dry-run` lists each company's steps and the most credits it could use, without running anything.
- **Example:** the 31-company run showed at most 475 credits beforehand. It used 181.

### Filling the important fields

#### 9. Staff count from the full-time count
- **Before:** if a report gave only "full-time equivalents" (FTE), the staff count was left empty.
- **Now:** the FTE number, rounded, is used, and the note says so.
- **Example:** 53 companies got a staff count (filled went from 58% to 81%).

#### 10. Size band when the share price has no date
- **Before:** without a date there was no exchange rate, so no size band.
- **Now:** the report's year-end date is used for the exchange rate.
- **Example:** 16 more companies got a size band.

#### 11. Currency names written the standard way
- **Before:** some older rows said "US$", "CA$" or "£", which the checks reject.
- **Now:** they say USD, CAD and GBP.
- **Example:** Avation, Amicorp and Aseana: 27 failed values now pass.

### Checking our work

#### 12. Numbers in tables drawn box by box
- **Before:** in some reports each table cell is a separate box, so the label and the number are never on one line. The quote check could not find them and failed the value.
- **Now:** if the number appears exactly once on its own in the document, on a page that also holds the label's words, it counts as found.
- **Example:** Flughafen Wien's pay table: 28 values are now verified.

#### 13. Re-checking without losing work done on the other laptop
- **Before:** re-checking all results on this laptop skipped quotes whose reports are stored on the other laptop. Real failures could quietly turn into passes.
- **Now:** those quotes keep the result they got on the other laptop.
- **Example:** 66 companies kept their honest scores.

#### 14. The dashboard follows our severity sheet
- **Before:** the dashboard used an older list of how important each field is, which differed from ours on 17 fields.
- **Now:** it reads importance (High, Medium, Low) and Required/Optional from the severity spreadsheet.
- **Example:** industry code and size band now show as High, not "Optional" or "Never used".

### Saving time

#### 15. Each PDF is converted once
- **Before:** the same report was converted twice, once by each part of the tool (minutes for a long report).
- **Now:** the second part reuses the first one's copy.
- **Example:** Tallink's 177-page report: no second 4-minute wait.

### Before the DACH runs

#### 16. One safe command to merge runs
- **Before:** runs were merged into the big combined file with throwaway scripts. Twice today that went wrong (runs mixed up; 74 values wiped).
- **Now:** `python -m extractor.combine` merges a run in: each company's rows replace its old ones, a field the run skipped never wipes a value, and the checks come along.
- **Example:** three people each run 125 companies and send their files; one command merges all three.

#### 17. Copy-protected PDFs can be read
- **Before:** some PDFs say "copying text not allowed". The table reader obeyed and skipped their pay tables.
- **Now:** the tool makes an unlocked copy and reads that.
- **Example:** 9 pay tables at Branicks, Cancom, Canal+ and Jinhui became readable.

#### 18. Input problems shown before the run
- **Before:** a bad input row was only noticed after the run had failed on it.
- **Now:** `--dry-run` lists, per company, links that need a login (Google Drive, SharePoint, OneDrive) and companies with no LEI or ISIN.
- **Example:** Wave 1's Google Drive links would have been flagged before spending credits.

#### 19. A warning when no credit cap is set
- **Before:** a run without `--max-run-credits` could spend without limit, silently.
- **Now:** the run says how many credits it could use when no cap is set.
- **Example:** "No --max-run-credits cap: this run could use up to 1,875 Firecrawl credits".

#### 20. A warning if the code changes during a run
- **Before:** editing the code while a run was going broke two companies (Bell Food, SED Energy) without any warning.
- **Now:** the run notices the change and prints a warning.
- **Example:** "WARNING: the code or prompts changed while this run is going".

### Getting ready for Swiss and German companies

#### 21. Searching the web for the report itself
- **Before:** the tool only looked on the company's main website. Swiss and German companies keep reports on a separate investor site, so it found nothing.
- **Now:** if the website has no recent report, the tool searches the web for "<company> annual report 2025" and keeps only the company's own documents.
- **Example:** Adidas's report on report.adidas-group.com, Bell's on bellfoodgroup.com, Arbonia's on its new domain.

#### 22. Even without a website
- **Before:** if no website was found, the report was never looked for.
- **Now:** the report is searched for by the company's name, and its site becomes the website.
- **Example:** APG SGA got its 2025 report.

#### 23. Reading German and French reports better
- **Before:** the words that pick which parts of a report the AI reads were English and Nordic only.
- **Now:** German, French and Italian words are included (Mitarbeitende, Umsatz, Verwaltungsrat, collaborateurs, chiffre d'affaires...), and Swiss numbers like 1'234'567.
- **Example:** a German-only report now sends its staff and pay pages to the AI.

#### 24. German share names cleaned
- **Before:** names like "Porsche AG VZO" or "BMW AG ST" were searched with the share type attached.
- **Now:** share-type endings (VZO, ST, INH, NA O.N.) are removed before searching.
- **Example:** "Porsche AG VZO" is searched as "Porsche".

#### 25. Three people running at once
- **Before:** if three computers asked the company register (GLEIF) too fast, it refused, and the company lost its ID.
- **Now:** the tool waits as long as GLEIF asks, then tries again.
- **Example:** three runs of 125 companies at the same time.

**Test on the 19 companies with no report:** 13 now have their 2025 report (11 of the 12 Swiss and German ones). Fiscal year filled went from 92% to 98%.

### Runs done today
- **Run 4 (19 companies, 52 credits):** 15 now read their 2025 report.
- **Run 5 (31 companies without a report, 181 credits):** 12 now have one. The other 19 still can't be found by the search; that needs separate work.

### Score on the High-importance fields
Share of companies with the field filled **and** passing every check:

| Field | Before | After |
|---|---|---|
| Staff count | 41% | 61% |
| Size band | 35% | 43% |
| Fiscal year | 88% | 92% |
| Total pay | 61% | 64% |
| Base salary | 75% | 77% |
| Revenue | 76% | 78% |

None went down.

### Still to do
- 19 companies whose report or website the search can't find (Adidas, BKW, Bell and others).
- Read more pay tables directly instead of through the AI: today only 25 of 194 companies use a table.
- Size band: 112 companies lack a share price or share count.

## 12 November 2026

After DACH Set 2 (102 companies, 64 Swiss and 61 German). Issue 19.

#### 26. Searching for the German "Geschäftsbericht" too
- **Before:** the web search only asked for "<name> annual report 2025 pdf". Small German companies often publish only in German, so it found nothing.
- **Now:** for a German, Swiss or Austrian company, when the English search finds nothing new, a second search asks for "<name> Geschäftsbericht 2025" (2 more credits).
- **Example:** Albis Leasing's 2025 report and 2invest's reports page turn up only in the German search.

#### 27. Small fixes to the report search
- **Before:** "Edisun Power Europe" wasn't matched to edisunpower.com (the domain leaves out "Europe"). "TISCON AG i.A." was searched as "tiscon ia". A title split across lines ("GESCHÄFTS- BERICHT 2025") wasn't read as a report.
- **Now:** place words (Europe, Swiss, Deutschland...) don't have to be in the domain. "i.A." / "i.L." (being wound up) are dropped from the name. Split titles are joined.
- **Example:** Edisun's investor page now counts as its own.

#### 28. "No variable pay" instead of "not found"
- **Before:** a board member paid only a salary had 7 empty bonus fields marked "not found", which looked like a failure.
- **Now:** when the total equals salary + benefits + pension and no bonus figure was read, those fields say "not applicable: no variable pay". Applied to saved results too, no re-run.
- **Example:** 2invest's sole board member: 72,000 salary, total 72,000. 70 values in 9 Set 2 companies (Uniper, which can't pay bonuses under state aid; ALSO's chairman; Dottikon's board).

#### 29. A failed re-run no longer overwrites good data
- **Before:** merging a run always took the newer rows. ABB's site blocked Set 2 (error 503), so ABB's pay dropped from 118 values to 3.
- **Now:** if a run gets under half the values already there for a company's facts or its pay, the old ones stay, and the merge says so. `--take-newer` overrides it.
- **Example:** re-merging Set 2 kept ABB's old pay and nothing else.

#### 30. Google Drive links are skipped, not misread
- **Before:** a Drive link gives a "view this file" page, not the PDF. Edisun's was read as its "2023 annual report".
- **Now:** links that need a sign-in (Google Drive, SharePoint, Dropbox...) are skipped, and the document is searched for instead.
- **Example:** Edisun no longer has a fake FY2023 report.

### Why Set 2 looked bad (and what wasn't really bad)
- Overall close to earlier runs: company facts 74% filled (76% before), pay 58% (62%).
- Most "missing" pay was fields small companies don't have: no bonus plan, or only totals published. Item 28 now marks the clear cases.
- Genuinely missing: 9 companies with no report found. Some have none to find (Accentro postponed its 2023 and 2024 accounts; TISCON is being wound up).
- Tracker links that don't work: Google Drive links (35 in Set 2) are private and need a sign-in, and a few links are broken (Viscom, Allgeier) or blocked (Barry Callebaut, Vincorion). These need the client to share public links.

### 12 November 2026 (later): what the AI reads, and quotes that failed (scraper version 2)

Measured first on the cached reports and the combined FY2025 file; no company was re-run yet.

#### 31. The AI reads the whole report
- **Before:** the report pass sent the AI short excerpts picked by keyword lists, 2,500 words per topic: a median 14% of a report (10,400 of 71,700 words, 407 reports). A value stated anywhere else stayed empty.
- **Now:** a report of up to 200,000 words is read whole (`REPORT_WORDS`); a longer one shares that budget between the topics. Fallback documents are read whole up to 60,000 words each (`DOC_WORDS`). The AI call may take up to 10 minutes (was 3).
- **Example:** adidas's key figures on pages 5-6 ("Number of employees 64,938", "EBITDA 3,124") were never sent.
- **Test:** 20 reports, every field asked afresh both ways: values with a verified quote 426 -> 493. Against saved numeric values that pass every check: 71 the same (was 64), 8 not given (was 18), 12 different (was 9).
- **Watch:** with the whole report in view the AI sometimes takes a headline revenue (Centrica's "business performance" revenue, EnQuest's "revenue and other operating income"). The prompt now names the income statement's revenue line; Balfour Beatty came right, the other two did not. Revenue normally comes from the tags or the financials step, not this pass.

#### 32. A second look at quotes that are not in the text
- **Before:** a value whose quote wasn't found word for word, or didn't print its figure, was graded C and left.
- **Now:** such values are shown to the AI again with the part of the document where they should be, and asked for the passage as printed (`extractor/requote.py`). The new quote is used only when it is in the text and prints the figure, and not when it is a figure on its own; the value never changes. `REQUOTE=0` turns it off.
- **Test:** on the saved answers of 30 reports, 65 quotes failed; 11 got a sound quote (8 of 15 company values, 3 of 50 pay values). A smaller gain than hoped: most of the rest are not quoting mistakes (see below).

#### 33. Text shapes that hid real quotes
- **Before:** some quotes were in the report but not matched: the PDF converter's "picture text" marks inside a sentence (in 609 of 2,768 cached texts), a full stop the font gives no character code ("45?5"), a footnote mark written "compensation4" or as a superscript, a word broken at a line end ("remain- ing").
- **Now:** the quote matcher reads through all four (`validate.normalize`, `quote_in_text`, `sections.strip_markup`).
- **Test:** the combined file scored again without saving: 18 quote checks fail -> pass, none pass -> fail; hard fails 1,122 -> 1,112. A first version that joined footnote marks to their word made 62 more fail and was replaced.

#### Still open after this (found by the second look)
- **Values the AI worked out:** "other members" = the table's total minus the CEO (Arbonia: 1,078 - 450 = 628); a head count from a list of names; "four members" written as a word. These need rules in code (a derived value with its formula; number words), not better quotes.
- **A quote that runs over a page break** with the page footer in between.
- **Saved notes keep only 160 characters of a quote**, so 96 failed quotes can't be checked again without a re-run.
- **Zero values** shown as a dash (71 hard fails) and **LTI values without a currency** (49): rule fixes. (Done in 34-36 below; the zeros turned out to be stated in words, not dashes.)

#### 34. Values in their quote that the check could not read
- **Before:** the "value in the quote" check (CORE-02) failed 437 values. Most were right:
  - a nil stated in words: "No bonuses were paid", "keine Mitarbeiter", "ikke foretatt tildeling" (71);
  - a count in words: "three employees", "zwei Prozent";
  - a decimal comma: "€ 2,14", "42,3";
  - a Swiss separator: "1′905′326", "98‘064";
  - cells grouped with spaces: "154 000 | 28 000";
  - "other members" worked out as the group total less the CEO, both in the quote.
- **Now:** the check reads all of these. A total less the CEO must match within 0.1%, not 0.5%: in a long row some pair of figures comes close by chance (Bachem's 435 - 173 = 262 is not 261).
- **Before:** when the AI gave the full amount and also the table's unit ("180000", thousands, for "£000 180"), the value was kept right but the note said "printed 180000 thousands". The check then looked for 180,000 in "£000 180", and the run graded these values C.
- **Now:** the printed figure is worked out (`extract.printed_figure`), at collection and when reading saved notes.
- **Test:** the combined file scored again without saving: CORE-02 fails 437 -> 205, hard fails 1,112 -> 902, none newly failing. Of 234 checks that turned to pass, 40 per kind were read by hand.
- **Not this check's job, seen on the way:**
  - two "EBITDA" values quote operating profit before tax (Holand og Setskog) and EBIT (Müller - Die lila Logistik);
  - two share prices are today's quote, not the year-end price (BayWa, Readcrest).

#### 35. Nothing paid needs no currency; a percentage is not an amount
- **Before:** a zero amount with no currency failed "unit is ISO 4217" and "same currency as the role's other amounts". "LTIP award of 200% of salary" was stored as an LTI granted of 200 with no currency.
- **Now:**
  - A zero amount needs no currency.
  - A pay amount printed only as a percentage is not stored; the note says it was stated only as a percentage. This applies from the next run.

#### 36. Quotes are kept whole
- **Before:** a note kept 160 characters of the quote. A longer quote could not be looked up again (96 failed checks).
- **Now:** up to 1,000 characters (`datapoints.QUOTE_CHARS`), from the next run.

### 12 November 2026 (evening): the version 2 trial, and two fixes it showed

The trial re-ran 30 companies (4 each from GB, CH, NO, SE, DE, DK; 3 each from AT, FI) under version 2 and compared them with their version 1 results under the same checks. 29 finished:
- values 1,767 -> 1,792
- hard fails 182 -> 82
- grade B 1,187 -> 1,312, grade C 353 -> 243

Kesko's version 1 values came from its FY2023 report; version 2 read FY2025.

#### 37. A page Firecrawl cannot get no longer holds up the run
- **Before:** Firecrawl answers a page it could not get with a server error ("Failed to scrape. All scraping engines failed"). The client retried that 6 times, so each SEB page took 10-20 minutes to give up, and SEB's run was stopped after an hour.
- **Now:**
  - That error is not retried.
  - A scrape may take 90 seconds.
  - A company's document fallback stops fetching after 10 minutes (`DOC_MINUTES`) and reads only cached documents after that.

#### 38. A profit line is not the revenue
- **Before:** Industrivärden's "Operating income 35,655" (its result, including the change in value of its holdings) was given as both its revenue and its EBITDA.
- **Now:**
  - The prompt says a profit line is never the revenue, and that an investment company with no revenue line has none.
  - In code, a revenue whose line label names a profit ("Operating profit", "Rörelseresultat", "Betriebsergebnis") is dropped. A label that also names revenue or the statement ("Statement of Profit or Loss ... management fees") is kept.
  - A revenue and an EBITDA of the same figure can't both be right. "Operating income" is a bank's total income (ProCredit) but an investment company's result, and the label can't tell which. So the EBITDA is dropped and the revenue is kept, graded C with a note to check it.
- **Test:** on the combined file, only ProCredit is affected (EBITDA dropped). Industrivärden re-run: no revenue and no EBITDA, total assets unchanged.

#### 39. A group role read from two documents is kept once
- **Before:** the remuneration report and the annual report's pay note print the same table, and the AI named the group row differently in each ("Other EC Members" and "Other EC", dormakaba; "Other IEC members" and "Übrige Mitglieder des IEC", Implenia). Both were kept, so the group's pay was counted twice. Found while checking PR #2 (a pay table's "Total" line, AXAC-379).
- **Now:** a group role whose amounts are the same as an earlier group role's, field for field, is left out: on a new run, and from saved rows when the CSV is next written. Rows of zeros and individual roles are left alone: two executives can be paid the same (Vontobel's co-CEOs).
- **Effect on the combined file:** 17 companies lose the second copy, among them Givaudan, Sandoz, Sartorius, Implenia, Bell Food, Straumann and dormakaba.

#### 40. A pay table's accounting line is not a person
- **Before:** S&D Standard's pay table has a section heading "Subsidiary employee:" over a line "Option and share program expenses (note 17)", with dashes for 2025. It was stored as an executive role paid 0.
- **Now:** an individual role is left out when every amount is zero and its quoted line names an expense, cost, provision or note, not a person. A person paid nothing stays: the combined file has 13 of them (Wild Bunch's CEO, Sino-German's board, United Eco Solutions' Vorstand).
- **Effect on the combined file:** S&D Standard only.

### 12 November 2026 (night): Revanth's PRs, reviewed and fixed

Both pull requests were run through a code review (`/code-review high`), the findings fixed on their branches, reviewed again, and merged into `main`.

#### 41. A pay table's "Total" line is not a role (PR #2, AXAC-379)
- **Before:** Brøndby IF's "Total" (CEO + CFO) and Stora Enso's "GLT Total" were stored as one more role, so the same pay was counted twice.
- **Now:** a group role whose amounts add up to two or more roles next to it is left out, on a new run and from saved rows.
  - It matches within 1%, or within the rounding of figures printed in millions up to 5% (CEO 1.4 + CFO 0.9 against a Total of 2.4).
  - Total pay alone counts only within 1%, otherwise two fields must add up. A lone figure in whole millions was matched by chance (BMW's "Board of Management 23 million").
  - A Total printed between its parts is found (Inficon: 606 + 365 = 971).
  - A run of only some pay fields no longer keeps part of an old Total role.
  - The pay prompt now says to leave out a total line of people listed one by one.
- **Effect on the combined file:** 41 companies lose a Total role. Checked by hand: Tekna, S&D Standard, dormakaba, Straumann, Sentia, Bilfinger.

#### 42. Company data from the documents the pay step read (PR #3, AXAC-379)
- **Before:** when the annual report could not be found (no website, or Firecrawl out of credits), every company field stayed empty, even when the run had downloaded a PDF that prints them (Stora Enso, Brøndby IF). The note "not found in: Annual report (PDF)" read as if that PDF had been searched.
- **Now:** the documents the pay step read are asked for the company fields still empty, one AI call per document and no Firecrawl.
  - They are read like the document fallback (`ask_documents`, now shared by both): yearly figures are year-checked, and an AI answer that runs too long skips the document instead of failing the company.
  - The legal name and country are checked, as for the annual report: a parent company's report is graded C.
  - A year end dates the figures only if it closes the pay year. A date other than 31 December must be quoted as the year end ("fiscal year", "for the year ended 31 March 2026"); Aurskog Sparebank's bonus-period end is not used.
  - This also runs when Firecrawl runs out during the pay step. A value it can only grade C is looked for again by the document fallback.
  - A field still empty says why first: "not found: the annual report was not read (...)".
- **Review:** the first review found 10 issues. Most came from the PR copying the document fallback without its rules, so the copy was replaced by the shared function rather than patched. A second review found 10 more, two of them mistakes in the first round of fixes (refusing "year ended" wording; a crash on an impossible date like 2025-06-31). All fixed.

#### 43. The SEB stall and the duplicate group roles, seen on the PRs
- Items 37 (a page Firecrawl cannot get) and 39-40 (duplicate group roles; an accounting line as a person) came out of checking these PRs. They are on `main` too.

### 13 November 2026: what the dashboard's "42% not found" is

The dashboard (built 12 November, 16:26, from `output/fy2025_runs_datapoints.csv`: 564 companies, nearly all collected by version 1) shows 42% of values not found and 56% found. Of all values:

| Cause | Share | What it is |
|---|---|---|
| Not found in the documents read | 22.9% | Real gaps, or fields the company doesn't disclose |
| **Not collected** | **16.2%** | The tracker's `run_required` asked only for the company's Pay Data or only its Company Data. These were never asked for, but the dashboard counts them as not found. |
| No annual report found | 1.7% | Real gaps |
| Missing inputs, no credits, API-only | 0.8% | |

Counting only the fields that were asked for, **30% are not found and about 67% found**.

Where the real gaps are:
- **Pay targets and maxima** (`sti_target`, `sti_max`, `lti_target`, `lti_max`): 35% of the gaps. Many companies, Nordic and DACH ones especially, don't state them as percentages.
- **LTI vested and granted:** 17% of the gaps.
  - 103 companies have no LTI figure for any executive, and 60 no STI figure: about 1,600 gaps.
  - Many of these companies may have no such plan, but a gap is only marked "not applicable" when the report clearly says so (item 28).

**Next steps:**
- **Free:**
  - the dashboard counts "not collected" as out of scope;
  - re-score the combined file with the current checks;
  - splice in the 29 trial companies.
- **Paid:**
  - the version 2 re-run of all companies;
  - asking the AI, with a quote, whether a company has an LTI or STI plan at all.
- **Later:** a share-price feed for share price and size band, missing for half the companies.

### 14 November 2026: the version 3 re-run

All three free steps above are done, and the plan question was added (item 44). Version 3 then re-ran every company whose results are on this machine: **289 of the 564**, in 9 hours, using **401 Firecrawl credits**. The other 278, mostly DACH sets 1 and 3, have their caches on other machines and are still on version 1.

#### 44. The AI is asked whether the executives have an STI or LTI plan
- The pay questions now also ask whether the company has a short-term and a long-term incentive plan for its executives.
- A plan is marked absent only when the report says so in words, and that sentence is kept as the quote, for example AEP Plantations: "No long-term incentive of the Company applies." The plan's fields are then `not applicable: no long-term incentive plan ("…")`, not "not found".
- When the report says nothing, the fields stay "not found". FastPartner, for one, was not marked.
- In this run, 498 fields at 40 companies were marked as having no plan.

#### 45. The dashboard leaves out fields that were not asked for
- Values noted `not collected` are fields the tracker's `run_required` never asked for (company data only, or pay only). The dashboard now counts them as not applicable, not as not found.

#### 46. A full amount in the quote passes CORE-02
- Sometimes the AI says a figure is in thousands when the text prints the full amount: Ceres Power's "£350,000" came back as 350 thousands. The stored value, 350,000, was right, but CORE-02 looked only for 350.
- CORE-02 now also passes when the stored full amount is in the quote. A different amount still fails: Computacenter's "£390,000" read as 130 thousands.

#### Results

| | Before (12 Nov) | After (14 Nov) |
|---|---|---|
| Found, all 564 companies | 56.0% | **70.4%** |
| Found, the 289 re-run | 59.8% | **71.9%** |
| Found, the 278 not re-run (scope fix only) | 52.3% | 68.8% |
| Checks passing | 98.0% | 98.3% |
| Failed checks | 2,959 | 2,515 |
| CORE-03 fails (quote not in the source) | 941 | 842 |
| CORE-02 fails (value not read off its quote) | 337 | 343 |

- **Most of the gain is the scope fix.** The 278 companies that were not re-run went from 52.3% to 68.8% with no new data.
- **What version 3 added, at the 289 re-run companies:**
  - 523 more values found;
  - 417 fewer partial values (12,906 → 13,429 found, 642 → 225 partial);
  - company-data gaps down from 4,105 to 2,124, and pay gaps from 3,941 to 2,909.
- **CORE-02 changed by six.** 163 new fails and 125 old ones gone. The new fails sampled are mostly real misreads the check now catches, such as a percentage read as an amount, or a sum of parts that doesn't match the stated total.
- **Ten companies kept their old pay rows,** because the new run found under half as many values: ABB, Addex, Alkemy, Basler Kantonalbank, Calida, Chesnara, Contango, Ostasiatiske, Pittler and Sino-German United. They are worth a look.

**Next:**
- re-run the other 278 on the machines that hold their caches, then merge them in with `python -m extractor.combine`;
- a share-price feed.
