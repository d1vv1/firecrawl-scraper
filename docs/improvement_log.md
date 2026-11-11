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
