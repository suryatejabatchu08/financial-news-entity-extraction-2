import json
import re
import random

# ==========================================
# FULL DATASET: 330 ANNOTATED EXAMPLES
# ==========================================
raw_data = [
    # --- BATCH 1: General Financial News (30) ---
    "In a surprise move on {Monday|DATE}, {Samsung Electronics|ORG} announced it would invest {45 trillion won|MONEY} into its semiconductor division.",
    "{Jane Fraser|PER}, the {CEO|ROLE} of {Citi|ORG}, warned that persistence inflation could force the {Fed|ORG} to keep rates high through {2025|DATE}.",
    "While the {S&P 500|ORG} rallied {1.2%|PERCENT}, shares in {Moderna|ORG} slipped after the {FDA|ORG} delayed its review.",
    "The merger between {Kroger|ORG} and {Albertsons|ORG}, valued at roughly {$24.6 billion|MONEY}, faces stiff antitrust scrutiny.",
    "Crude oil futures dipped below {$70|MONEY} per barrel for the first time since {December 2023|DATE} due to weak demand from {China|ORG}.",
    "{Masayoshi Son|PER} stated that {SoftBank|ORG} is shifting its focus entirely to AI, targeting a {15%|PERCENT} IRR for the upcoming fiscal year.",
    "Regulatory filings from {Q3|DATE} reveal that {Berkshire Hathaway|ORG} trimmed its stake in {BYD|ORG} by another {2.5 million|MONEY} shares.",
    "{Christine Lagarde|PER}, {President|ROLE} of the {European Central Bank|ORG}, hinted at a potential {25 basis point|PERCENT} cut in {June|DATE}.",
    "Post-market trading saw {Coinbase|ORG} jump {6%|PERCENT} after {Bitcoin|ORG} reclaimed the {$65,000|MONEY} level.",
    "The {Department of Justice|ORG} is seeking more than {$4 billion|MONEY} in penalties from {Binance|ORG}.",
    "Analysts at {Goldman Sachs|ORG} have downgraded {Rio Tinto|ORG} to 'Neutral', citing a {10%|PERCENT} drop in iron ore prices.",
    "Starting {next month|DATE}, {Neal Mohan|PER}, the {CEO|ROLE} of {YouTube|ORG}, plans to introduce new monetization tiers.",
    "Despite a {40%|PERCENT} year-over-year revenue increase, {Nvidia|ORG} shares remained flat on {Tuesday|DATE}.",
    "The {Bank of Japan|ORG} ended its negative interest rate policy, raising the short-term rate to a range of {0 to 0.1%|PERCENT}.",
    "German chemical giant {BASF|ORG} is cutting {2,600|MONEY} jobs to save {€500 million|MONEY} annually.",
    "Led by {CEO|ROLE} {Satya Nadella|PER}, {Microsoft|ORG} has committed {$2.9 billion|MONEY} to build data centers in {Japan|ORG}.",
    "Inflation in the {Eurozone|ORG} cooled to {2.4%|PERCENT} in {March|DATE}, defying expectations of a sticky {2.6%|PERCENT}.",
    "{Evergrande|ORG}'s liquidation order has sent shockwaves through the property sector, wiping out {$300 billion|MONEY} in value.",
    "{Thierry Breton|PER}, the {EU internal market commissioner|ROLE}, demanded that {TikTok|ORG} spare no effort to protect teenagers.",
    "As of {Friday|DATE}, the {10-year Treasury yield|ORG} spiked to {4.5%|PERCENT}, pressuring growth stocks.",
    "{Saudi Aramco|ORG} declared a dividend payout of {$31 billion|MONEY} despite a slide in quarterly profits.",
    "Venture capital funding in the fintech sector plummeted {35%|PERCENT} in {2024|DATE} compared to the previous year.",
    "{Lina Khan|PER}, {Chair|ROLE} of the {FTC|ORG}, blocked the acquisition on grounds that it would harm competition.",
    "{SpaceX|ORG} insiders claim the company's valuation has now topped {$180 billion|MONEY} following the secondary sale.",
    "Indian conglomerate {Reliance Industries|ORG} secured a deal with {Disney|ORG} to merge their media assets on {February 28|DATE}.",
    "The {IMF|ORG} raised its global growth forecast to {3.2%|PERCENT} but warned of geopolitical risks.",
    "{Larry Fink|PER}, {Chairman|ROLE} of {BlackRock|ORG}, emphasized the need for energy pragmatism in his annual letter.",
    "The {United Auto Workers|ORG} union secured a {25%|PERCENT} wage hike over four years after the strike against {Ford|ORG}.",
    "{Zurich Insurance|ORG} posted a record operating profit of {$3.7 billion|MONEY}, driven by strong underwriting.",
    "On {Wednesday|DATE}, {OpenAI|ORG} confirmed that {Sam Altman|PER} would return as {CEO|ROLE}.",

    # --- BATCH 2: Legal & Regulatory (30) ---
    "In a landmark ruling on {Tuesday|DATE}, {Judge James Boasberg|PER} dismissed the {FTC|ORG}'s antitrust lawsuit against {Meta|ORG}, stating the company faces fierce competition from {TikTok|ORG}.",
    "The {Irish Data Protection Commission|ORG} slapped {TikTok|ORG} with a record {€530 million|MONEY} fine for mishandling the data of teenagers.",
    "{Google|ORG} is preparing its final appeal against the {DOJ|ORG}'s order to divest its ad-tech business, arguing the breakup would harm small businesses.",
    "The {SEC|ORG} charged {Ryan Squillante|PER}, a former {Head of Equity Trading|ROLE}, with insider trading that allegedly generated {$216,000|MONEY} in illicit profits.",
    "Biopharma firm {FibroGen|ORG} agreed to pay {$1.25 million|MONEY} to settle charges that it misled investors about the safety data of its anemia drug, {Roxadustat|ORG}.",
    "{Lina Khan|PER}, the {Chair|ROLE} of the {FTC|ORG}, vowed to appeal the decision, emphasizing that big tech monopolies stifle innovation.",
    "On {September 5|DATE}, the {European Commission|ORG} designated {Booking.com|ORG} as a 'gatekeeper' under the Digital Markets Act, forcing it to comply with stricter interoperability rules.",
    "Shareholders of {Tesla|ORG} are suing the board, claiming that excessive compensation packages diluted their equity by {3%|PERCENT} in {2024|DATE}.",
    "The {Supreme Court|ORG} declined to hear the appeal regarding the patent dispute between {Novo Nordisk|ORG} and {Dr. Reddy's Laboratories|ORG} over the weight-loss drug {Wegovy|ORG}.",
    "Federal prosecutors seized {$198 million|MONEY} in assets from {PGI Global|ORG}, labeling the operation a 'classic Ponzi scheme' targeting retail crypto investors.",
    "Citing 'systemic failures' in anti-money laundering controls, the {FCA|ORG} fined {Barclays|ORG} {£26 million|MONEY} on {Wednesday|DATE}.",
    "The {Department of Justice|ORG} has opened a criminal probe into {UnitedHealth|ORG} regarding potential overcharging of the {Medicare|ORG} program.",
    "{OpenAI|ORG} faces a new class-action lawsuit filed in {California|ORG}, alleging it scraped copyrighted material from {New York Times|ORG} without compensation.",
    "Regulators in {South Korea|ORG} fined {Goldman Sachs|ORG} and {BNP Paribas|ORG} a combined {$20 million|MONEY} for naked short-selling violations.",
    "Despite the plea, {Judge Leonie Brinkema|PER} ruled that {Google|ORG} holds two illegal monopolies in the search market.",
    "The {Consumer Financial Protection Bureau|ORG} banned {Unicoin|ORG} from operating in the US after it falsely claimed its tokens were backed by real estate assets.",
    "Starting {January 1, 2026|DATE}, the {Basel III|ORG} endgame capital requirements will force US banks to hold {19%|PERCENT} more capital.",
    "{Universal Music Group|ORG} sued AI startup {Anthropic|ORG} for {$75 million|MONEY}, claiming widespread copyright infringement in its training data.",
    "The {EPA|ORG} announced a settlement with {Norfolk Southern|ORG}, requiring the rail giant to pay {$310 million|MONEY} for the environmental cleanup.",
    "In a blow to {Bayer|ORG}, a jury in {Philadelphia|ORG} awarded {$2.25 billion|MONEY} to a plaintiff who claimed the weedkiller Roundup caused his cancer.",
    "{Gary Gensler|PER}, the {Chairman|ROLE} of the {SEC|ORG}, warned that 'AI-washing' in investment prospectuses would face strict enforcement actions.",
    "The {UK Competition and Markets Authority|ORG} blocked the acquisition of {Activision|ORG} by {Microsoft|ORG} before reversing its decision on {October 13|DATE}.",
    "{Binance|ORG}'s founder {Changpeng Zhao|PER} was sentenced to four months in prison after pleading guilty to violating the Bank Secrecy Act.",
    "The {European Central Bank|ORG} revoked the banking license of {Pilatus Bank|ORG} following the arrest of its {Chairman|ROLE} on money laundering charges.",
    "A federal judge in {Texas|ORG} struck down the {National Labor Relations Board|ORG}'s new rule on joint-employer status, calling it 'overly broad'.",
    "{Amazon|ORG} defeated a proposed class action claiming it inflated the prices of e-books in collusion with major publishers.",
    "The {Commodity Futures Trading Commission|ORG} ordered {Coinbase|ORG} to pay a {$6.5 million|MONEY} penalty for reporting false trading data.",
    "{China|ORG}'s internet watchdog imposed a {$1.2 billion|MONEY} fine on ride-hailing giant {Didi Global|ORG} for violating data security laws.",
    "On {Monday|DATE}, the {Supreme Court of India|ORG} rejected the plea by {Vodafone Idea|ORG} to recalculate its adjusted gross revenue dues.",
    "{Wells Fargo|ORG} disclosed it has set aside an additional {$1 billion|MONEY} for potential legal settlements related to its legacy fake accounts scandal.",

    # --- BATCH 3: Emerging Markets & Commodities (30) ---
    "Copper futures on the {LME|ORG} surged to {$9,000|MONEY} per tonne on {Friday|DATE} amid supply disruptions in {Panama|ORG}.",
    "{Petrobras|ORG} shares plunged {6%|PERCENT} after the Brazilian government hinted at changing the dividend policy on {May 14|DATE}.",
    "The {South African Reserve Bank|ORG} kept its main lending rate at {8.25%|PERCENT}, citing persistent food inflation.",
    "{Codelco|ORG}, the world's largest copper producer, reported a production slump to {1.32 million tonnes|MONEY} in {2023|DATE}.",
    "Indonesia's ban on nickel ore exports has forced foreign investors to pour {$15 billion|MONEY} into local smelters since {2020|DATE}.",
    "The {Turkish Lira|ORG} hit a record low of {32.6|MONEY} against the dollar, pressuring the central bank to hike rates to {50%|PERCENT}.",
    "{Saudi Aramco|ORG} {CEO|ROLE} {Amin Nasser|PER} said the energy transition is failing and demand for oil will continue rising.",
    "Spot gold prices breached the {$2,400|MONEY} mark on {April 12|DATE} as geopolitical tensions in the Middle East escalated.",
    "Argentina's monthly inflation slowed to {11%|PERCENT} in {March|DATE}, a win for President {Javier Milei|PER}'s austerity measures.",
    "Australian miner {BHP Group|ORG} offered {$39 billion|MONEY} to acquire {Anglo American|ORG} to secure access to its copper mines.",
    "India's {Reliance Industries|ORG} became the first Indian company to hit a market cap of {₹20 lakh crore|MONEY} on {Tuesday|DATE}.",
    "Wheat prices jumped {4%|PERCENT} after {Russia|ORG} targeted grain infrastructure in the {Odesa|ORG} port region.",
    "{Vale|ORG} admitted that iron ore output at its S11D mine was {5%|PERCENT} below targets due to heavy rains in the {Amazon|ORG}.",
    "The {Nigerian National Petroleum Company|ORG} is seeking a {$2 billion|MONEY} loan to boost LNG production.",
    "Cocoa futures skyrocketed to over {$10,000|MONEY} per metric ton for the first time in history on {Tuesday|DATE} due to poor harvests in {Ghana|ORG}.",
    "{Antofagasta|ORG} agreed to invest {$4.4 billion|MONEY} to expand its Centinela copper mine in {Chile|ORG}.",
    "Vietnam's {VinFast|ORG} is delaying its {$4 billion|MONEY} factory construction in {North Carolina|ORG} until {2025|DATE}.",
    "The {Bank of Japan|ORG} intervened in the currency market after the yen weakened to {160|MONEY} against the dollar on {Monday|DATE}.",
    "Russian gas giant {Gazprom|ORG} reported a net loss of {$6.9 billion|MONEY} for {2023|DATE}, its first annual loss in decades.",
    "{Mexico|ORG}'s state oil company {Pemex|ORG} received a {$8 billion|MONEY} tax break to help manage its massive debt load.",
    "Rare earth miner {Lynas|ORG} saw its profits drop {74%|PERCENT} as prices for Neodymium tumbled in {China|ORG}.",
    "{Ngozi Okonjo-Iweala|PER}, the {Director-General|ROLE} of the {WTO|ORG}, warned that fragmentation could cost the global economy {5%|PERCENT} of GDP.",
    "Abu Dhabi's {Adnoc|ORG} formally approached {Covestro|ORG} with a takeover offer valued at {€11 billion|MONEY}.",
    "Inflation in {Egypt|ORG} soared to {35.7%|PERCENT} in {February|DATE} following the central bank's decision to float the pound.",
    "{Glencore|ORG} is planning to spin off its coal business after acquiring a {77%|PERCENT} stake in {Teck Resources|ORG}' steelmaking coal unit.",
    "On {Wednesday|DATE}, {BYD|ORG} overtook {Tesla|ORG} as the top-selling EV brand in {Singapore|ORG}.",
    "{TotalEnergies|ORG} signed a deal to develop a {$10 billion|MONEY} offshore oil project in {Suriname|ORG}.",
    "The {People's Bank of China|ORG} injected {100 billion yuan|MONEY} into the banking system to maintain liquidity.",
    "Shares in {First Quantum Minerals|ORG} crashed {50%|PERCENT} after {Panama|ORG}'s Supreme Court ruled its mining contract unconstitutional.",
    "{Kristalina Georgieva|PER}, {Managing Director|ROLE} of the {IMF|ORG}, approved a {$1.1 billion|MONEY} disbursement to {Pakistan|ORG}.",

    # --- BATCH 4: Executives & Roles (30) ---
    "Effective {January 1|DATE}, {Jane Fraser|PER} will assume the role of {Chief Executive Officer|ROLE} at {Citigroup|ORG}, succeeding {Michael Corbat|PER}.",
    "{Goldman Sachs|ORG} announced that {David Solomon|PER} has been appointed as {Chairman|ROLE} of the board, in addition to his current duties as {CEO|ROLE}.",
    "In an interview with Bloomberg on {Tuesday|DATE}, {Larry Fink|PER}, the {CEO|ROLE} of {BlackRock|ORG}, discussed the future of sustainable investing.",
    "The board of directors at {Wells Fargo|ORG} has named {Charlie Scharf|PER} as the new {CEO|ROLE} and {President|ROLE}, effective immediately.",
    "{Morgan Stanley|ORG} promoted {Ted Pick|PER} to {Co-President|ROLE}, positioning him as a potential successor to current {CEO|ROLE} {James Gorman|PER}.",
    "{JPMorgan Chase|ORG} {CEO|ROLE} {Jamie Dimon|PER} will share his annual shareholder letter on {Wednesday|DATE}.",
    "Former {Bank of England|ORG} governor {Mark Carney|PER} has joined {Brookfield Asset Management|ORG} as {Vice Chair|ROLE} and {Head of Transition Investing|ROLE}.",
    "{Mary Barra|PER}, {CEO|ROLE} of {General Motors|ORG}, stated that the company plans to invest {$35 billion|MONEY} in electric and autonomous vehicles through {2025|DATE}.",
    "Following the departure of {Jeff Bezos|PER}, {Andy Jassy|PER} took over as {CEO|ROLE} of {Amazon|ORG} in {Q3 2021|DATE}.",
    "{Tesla|ORG} 's {Technoking|ROLE}, {Elon Musk|PER}, indicated that the company might resume accepting {Bitcoin|ORG} for vehicle purchases.",
    "{Sundar Pichai|PER}, {CEO|ROLE} of {Alphabet|ORG} and {Google|ORG}, announced a new {AI|ORG} research hub in {Paris|ORG}.",
    "{IMF|ORG} has appointed {Gita Gopinath|PER} as its {First Deputy Managing Director|ROLE}, the second-highest position at the fund.",
    "{Christine Lagarde|PER}, {President|ROLE} of the {European Central Bank|ORG}, warned about the economic impact of rising energy prices.",
    "{Satya Nadella|PER}, {Chairman|ROLE} and {CEO|ROLE} of {Microsoft|ORG}, emphasized the importance of cloud computing in the company's earnings call.",
    "{Berkshire Hathaway|ORG} {Vice Chairman|ROLE} {Charlie Munger|PER} passed away at the age of 99 on {Tuesday|DATE}.",
    "{Tim Cook|PER}, {CEO|ROLE} of {Apple|ORG}, unveiled the new Vision Pro headset at the company's Worldwide Developers Conference.",
    "{Meta|ORG} {COO|ROLE} {Sheryl Sandberg|PER} stepped down from her role after 14 years at the company.",
    "{Nvidia|ORG} founder and {CEO|ROLE} {Jensen Huang|PER} delivered a keynote address on the future of AI at the GTC conference.",
    "{UBS|ORG} has re-appointed {Sergio Ermotti|PER} as {Group Chief Executive Officer|ROLE} to lead the integration of {Credit Suisse|ORG}.",
    "{HSBC|ORG} appointed {Georges Elhedery|PER} as its new {Group Chief Financial Officer|ROLE}, effective {January 1, 2023|DATE}.",
    "Former {U.S.|ORG} Treasury Secretary {Hank Paulson|PER} has joined the board of directors at {TPG Capital|ORG}.",
    "{Ken Griffin|PER}, founder and {CEO|ROLE} of {Citadel|ORG}, was interviewed about the impact of retail trading on market volatility.",
    "{Bridgewater Associates|ORG} named {Nir Bar Dea|PER} as its sole {CEO|ROLE} following a leadership restructuring.",
    "{Apollo Global Management|ORG} co-founder {Marc Rowan|PER} has taken over as {CEO|ROLE} after the departure of {Leon Black|PER}.",
    "{Blackstone|ORG} {President|ROLE} {Jon Gray|PER} said the firm sees significant opportunities in the real estate sector.",
    "{Carlyle Group|ORG} appointed {Harvey Schwartz|PER}, a former {Goldman Sachs|ORG} executive, as its new {CEO|ROLE}.",
    "{KKR|ORG} co-founders {Henry Kravis|PER} and {George Roberts|PER} have stepped down as co-CEOs, handing the reins to {Joe Bae|PER} and {Scott Nuttall|PER}.",
    "{Visa|ORG} announced that {Ryan McInerney|PER} would become {CEO|ROLE} on {February 1, 2023|DATE}, succeeding {Al Kelly|PER}.",
    "{Mastercard|ORG} {CEO|ROLE} {Michael Miebach|PER} discussed the company's strategy for digital payments and cryptocurrency.",
    "{PayPal|ORG} pointed to {Alex Chriss|PER} as its new {President|ROLE} and {CEO|ROLE}, effective {September 27, 2023|DATE}.",

    # --- BATCH 5: Earnings Reports (30) ---
    "{Alphabet|ORG} shares slid {4%|PERCENT} after the company reported {Q3|DATE} ad revenue of {$59.6 billion|MONEY}, missing estimates.",
    "Despite supply chain woes, {Ford|ORG} posted an adjusted earnings per share of {$0.49|MONEY}, beating the consensus of {$0.30|MONEY}.",
    "{Salesforce|ORG} raised its full-year revenue guidance to {$38 billion|MONEY}, sending the stock up {3%|PERCENT} in extended trading.",
    "On {Thursday|DATE}, {Netflix|ORG} announced it added {5.9 million|MONEY} net new subscribers in the third quarter.",
    "{Walmart|ORG} warned that consumer spending is softening, predicting a flat same-store sales growth for {Q4 2025|DATE}.",
    "{Pfizer|ORG} reported a net loss of {$2.4 billion|MONEY} for the quarter, largely due to write-offs related to its Covid inventory.",
    "Analysts were impressed by {Palantir|ORG}'s {20%|PERCENT} year-over-year growth in commercial revenue reported on {Monday|DATE}.",
    "{Delta Air Lines|ORG} sees record travel demand, projecting revenue of {$14 billion|MONEY} for the holiday quarter ending {December 31|DATE}.",
    "{Taiwan Semiconductor|ORG} confirmed that revenue for {October|DATE} jumped {34.8%|PERCENT} thanks to booming AI chip demand.",
    "{Disney|ORG} plans to cut costs by another {$2 billion|MONEY} after its streaming division lost {$387 million|MONEY} in the recent quarter.",
    "{Goldman Sachs|ORG} reported a {33%|PERCENT} slump in profits to {$2.06 billion|MONEY}, hit by a slowdown in dealmaking.",
    "Shares of {Snap|ORG} plummeted {14%|PERCENT} after the social media firm warned that ad revenue would be flat in {Q4|DATE}.",
    "{ExxonMobil|ORG} delivered a massive {$9.1 billion|MONEY} profit for {Q3 2025|DATE}, fueled by rising crude prices.",
    "{Visa|ORG} announced a new share buyback program of {$25 billion|MONEY} alongside its quarterly earnings beat.",
    "{Spotify|ORG} finally turned a profit, posting an operating income of {€32 million|MONEY} for the first time since {2021|DATE}.",
    "{Intel|ORG} provided a gloomy forecast for {Q1 2026|DATE}, expecting revenue between {$12.2 billion|MONEY} and {$13.2 billion|MONEY}.",
    "{Caterpillar|ORG} stock rose {5%|PERCENT} as the industrial giant reported record free cash flow of {$3 billion|MONEY}.",
    "{Novo Nordisk|ORG} raised its sales outlook for {Wegovy|ORG} by {15%|PERCENT} following strong demand in the {US|ORG}.",
    "{Starbucks|ORG} reported that global comparable store sales rose {8%|PERCENT}, driven by a {5%|PERCENT} increase in average ticket size.",
    "{AMD|ORG} forecasted AI chip sales of {$2 billion|MONEY} for {2026|DATE}, signaling a strong challenge to {Nvidia|ORG}.",
    "{HSBC|ORG} announced a special dividend of {$0.21|MONEY} per share after pre-tax profits surged to {$7.7 billion|MONEY}.",
    "{Uber|ORG} posted its first-ever annual operating profit of {$1.1 billion|MONEY}, marking a turning point for the ride-hailing giant.",
    "{LVMH|ORG} saw organic revenue growth slow to {9%|PERCENT} in {Q3|DATE} as luxury demand cooled in {Europe|ORG}.",
    "{Airbnb|ORG} noted that average daily rates rose to {$161|MONEY} in the quarter, driving revenue to {$3.4 billion|MONEY}.",
    "{Target|ORG} shares surged {17%|PERCENT} after the retailer reported much better-than-feared margins for {Q3|DATE}.",
    "{Alibaba|ORG} scrapped plans to spin off its cloud unit, causing the stock to drop {10%|PERCENT} on {Thursday|DATE}.",
    "{Boeing|ORG} narrowed its loss to {$1.6 billion|MONEY} but lowered its delivery target for the 737 Max.",
    "{Arm Holdings|ORG} issued bullish guidance for {fiscal 2026|DATE}, expecting revenue to top {$3 billion|MONEY}.",
    "{Lowe's|ORG} cut its full-year sales forecast, citing a pullback in DIY spending by homeowners.",
    "{Zoom|ORG} reported enterprise revenue of {$660 million|MONEY}, up {7.5%|PERCENT} year-over-year.",

    # --- BATCH 6: M&A / Deals (30) ---
    "{Broadcom|ORG} finally closed its {$69 billion|MONEY} acquisition of {VMware|ORG} on {Wednesday|DATE} after receiving regulatory clearance.",
    "{Chevron|ORG} announced a definitive agreement to acquire {Hess|ORG} in an all-stock transaction valued at {$53 billion|MONEY}.",
    "{Adobe|ORG} terminated its {$20 billion|MONEY} merger with {Figma|ORG} due to pressure from the {UK|ORG} and {EU|ORG} regulators.",
    "{Macy's|ORG} rejected a {$5.8 billion|MONEY} buyout offer from {Arkhouse Management|ORG} and {Brigade Capital|ORG}.",
    "{Bristol Myers Squibb|ORG} agreed to buy neuroscience drugmaker {Karuna Therapeutics|ORG} for {$14 billion|MONEY}.",
    "{Nippon Steel|ORG} clinched a deal to buy {US Steel|ORG} for {$14.9 billion|MONEY}, creating a global steel giant.",
    "{BlackRock|ORG} intends to acquire {Global Infrastructure Partners|ORG} for roughly {$12.5 billion|MONEY} in cash and stock.",
    "{HPE|ORG} is nearing a deal to buy {Juniper Networks|ORG} for approximately {$13 billion|MONEY}.",
    "{Synopsys|ORG} will acquire engineering software firm {Ansys|ORG} for {$35 billion|MONEY} in a cash-and-stock deal.",
    "{Capital One|ORG} announced it would acquire {Discover Financial|ORG} in a {$35.3 billion|MONEY} all-stock deal.",
    "{Truist Financial|ORG} agreed to sell its insurance brokerage unit to an investor group for {$15.5 billion|MONEY}.",
    "{Home Depot|ORG} struck a deal to buy {SRS Distribution|ORG} for {$18.25 billion|MONEY} to expand its pro business.",
    "{Johnson & Johnson|ORG} completed the spinoff of its consumer health unit, {Kenvue|ORG}, on {August 23|DATE}.",
    "{Cisco|ORG} completed its {$28 billion|MONEY} acquisition of cybersecurity firm {Splunk|ORG} earlier than expected.",
    "{Diamondback Energy|ORG} agreed to buy privately held {Endeavor Energy Resources|ORG} in a {$26 billion|MONEY} deal.",
    "{Walmart|ORG} is buying smart TV maker {Vizio|ORG} for {$2.3 billion|MONEY} to boost its ad business.",
    "{Thoma Bravo|ORG} completed the take-private acquisition of {Everbridge|ORG} for {$1.5 billion|MONEY}.",
    "{Reddit|ORG} launched its IPO on {Thursday|DATE}, valuing the social media platform at {$6.4 billion|MONEY}.",
    "{Rubrik|ORG}, a cloud data security firm backed by {Microsoft|ORG}, is planning an IPO to raise {$750 million|MONEY}.",
    "{Permira|ORG} and {Blackstone|ORG} proposed a roughly {€14 billion|MONEY} buyout of online classifieds group {Adevinta|ORG}.",
    "{Smurfit Kappa|ORG} agreed to merge with {WestRock|ORG} to create a packaging giant worth {$20 billion|MONEY}.",
    "{Qualcomm|ORG} terminated its bid to acquire {Autotalks|ORG} citing regulatory hurdles.",
    "{Pfizer|ORG} completed its {$43 billion|MONEY} acquisition of cancer drugmaker {Seagen|ORG} on {December 14|DATE}.",
    "{KKR|ORG} acquired the remaining {37%|PERCENT} stake in {Global Atlantic|ORG} for {$2.7 billion|MONEY}.",
    "{Paramount Global|ORG} has entered exclusive merger talks with {Skydance Media|ORG}, sources told {CNBC|ORG}.",
    "{Liberty Media|ORG} announced plans to split into two tracking stocks to unlock value in {SiriusXM|ORG}.",
    "{Unilever|ORG} announced it would spin off its ice cream division, which includes {Ben & Jerry's|ORG}, by the end of {2025|DATE}.",
    "{BBVA|ORG} launched a hostile takeover bid for rival Spanish bank {Sabadell|ORG} valued at {€12 billion|MONEY}.",
    "{ConocoPhillips|ORG} agreed to buy {Marathon Oil|ORG} in a {$22.5 billion|MONEY} all-stock transaction.",
    "{T-Mobile|ORG} announced a {$4.4 billion|MONEY} deal to acquire {US Cellular|ORG}'s wireless operations.",

    # --- BATCH 7: Analyst Ratings (30) ---
    "{Morgan Stanley|ORG} raised its price target on {Nvidia|ORG} to {$1,200|MONEY}, citing accelerating demand for its H100 chips.",
    "Shares of {Snowflake|ORG} dropped {5%|PERCENT} after {Piper Sandler|ORG} downgraded the stock to 'Neutral' from 'Overweight'.",
    "{Wedbush|ORG} analyst {Dan Ives|PER} maintained an 'Outperform' rating on {Tesla|ORG} with a {$300|MONEY} price target.",
    "{Bank of America|ORG} reiterated its 'Buy' rating on {Apple|ORG} ahead of the {September|DATE} product launch event.",
    "{Citi|ORG} opened a 'negative catalyst watch' on {Intel|ORG}, predicting a revenue miss in {Q4 2025|DATE}.",
    "Analysts at {Jefferies|ORG} slashed their target for {Lululemon|ORG} to {$350|MONEY}, warning of slowing apparel demand.",
    "{Barclays|ORG} upgraded {FedEx|ORG} to 'Equal Weight' and raised the target price to {$290|MONEY}.",
    "{JPMorgan|ORG} sees {Amazon|ORG} as a 'Top Pick' for {2026|DATE}, forecasting {15%|PERCENT} upside from current levels.",
    "{Bernstein|ORG} analyst {Toni Sacconaghi|PER} questioned the valuation of {Palantir|ORG}, setting a price target of just {$10|MONEY}.",
    "{Wolfe Research|ORG} downgraded {Paramount Global|ORG} to 'Underperform', citing concerns over its linear TV exposure.",
    "{Goldman Sachs|ORG} initiated coverage on {Arm Holdings|ORG} with a 'Buy' rating and a {$85|MONEY} price objective.",
    "{Needham|ORG} raised its forecast for {Uber|ORG}, expecting gross bookings to grow {20%|PERCENT} year-over-year.",
    "{Deutsche Bank|ORG} lowered its price target on {Boeing|ORG} to {$225|MONEY} following the latest manufacturing delays.",
    "{Mizuho|ORG} analyst {Vijay Rakesh|PER} believes {Micron|ORG} is well-positioned to benefit from the HBM3 shortage.",
    "{Evercore ISI|ORG} added {Salesforce|ORG} to its 'Tactical Outperform' list ahead of earnings on {Wednesday|DATE}.",
    "{Redburn Atlantic|ORG} downgraded {Disney|ORG} to 'Sell', forecasting continued losses in the DTC segment.",
    "{UBS|ORG} raised its target for {Netflix|ORG} to {$700|MONEY}, praising the success of its ad-supported tier.",
    "{Truist|ORG} cut its rating on {Rivian|ORG} to 'Hold', noting significant cash burn risks through {2025|DATE}.",
    "{Raymond James|ORG} upgraded {SoFi Technologies|ORG} to 'Market Perform' after the recent pullback in share price.",
    "{KeyBanc|ORG} maintained an 'Overweight' rating on {CrowdStrike|ORG}, citing strong cybersecurity spending trends.",
    "{Oppenheimer|ORG} analyst {Rick Schafer|PER} raised his target on {NXP Semiconductors|ORG} to {$280|MONEY}.",
    "{Moody's|ORG} downgraded the credit outlook for {New York Community Bancorp|ORG} to 'Negative' on {Friday|DATE}.",
    "{Stifel|ORG} expects {Delta Air Lines|ORG} to generate {$4 billion|MONEY} in free cash flow in {2025|DATE}.",
    "{Cowen|ORG} reiterated its 'Outperform' rating on {Costco|ORG}, calling it a defensive staple in a volatile market.",
    "{CFRA|ORG} raised its opinion on {General Motors|ORG} to 'Buy' after the company announced a {$10 billion|MONEY} buyback.",
    "{Guggenheim|ORG} lowered its price target for {Pfizer|ORG} to {$28|MONEY}, reflecting weak sales of its Covid portfolio.",
    "{Loop Capital|ORG} upgraded {Pinterest|ORG} to 'Buy', arguing that ad monetization is improving faster than expected.",
    "{Baird|ORG} analyst {Colin Sebastian|PER} maintained a 'Neutral' rating on {Etsy|ORG}, citing headwinds in consumer discretionary spend.",
    "{HSBC|ORG} downgraded {Nike|ORG} to 'Hold', warning of increasing competition from {On Running|ORG} and {Hoka|ORG}.",
    "{RBC Capital|ORG} raised its target for {Shopify|ORG} to {$95|MONEY}, expecting strong GMV growth in the holiday season.",

    # --- BATCH 8: Macroeconomics (30) ---
    "The {US|ORG} economy added {275,000|MONEY} jobs in {November|DATE}, smashing estimates of {190,000|MONEY}.",
    "Inflation as measured by the CPI rose {3.2%|PERCENT} year-over-year in {February|DATE}, slightly higher than the {3.1%|PERCENT} forecast.",
    "The {Federal Reserve|ORG} held interest rates steady at {5.25%-5.50%|PERCENT} but signaled three rate cuts for {2026|DATE}.",
    "US GDP grew at an annualized rate of {1.6%|PERCENT} in {Q1|DATE}, marking a significant slowdown from the previous quarter.",
    "The {European Central Bank|ORG} cut its deposit rate by {25 basis points|PERCENT} to {3.75%|PERCENT} on {Thursday|DATE}.",
    "Initial jobless claims rose to {221,000|MONEY} for the week ending {March 30|DATE}, the highest level in two months.",
    "The {Bank of England|ORG} voted 7-2 to keep the base rate at {5.25%|PERCENT}, stating inflation remains 'sticky'.",
    "{China|ORG}'s manufacturing PMI fell to {49.5|MONEY} in {May|DATE}, indicating a contraction in factory activity.",
    "Retail sales in the {US|ORG} were flat in {April|DATE}, missing the economist consensus of a {0.4%|PERCENT} increase.",
    "The {Institute for Supply Management|ORG} services index dipped to {51.4|MONEY} in {March|DATE}, driven by lower new orders.",
    "Core PCE, the {Fed|ORG}'s preferred inflation gauge, cooled to {2.8%|PERCENT} on an annual basis in {February|DATE}.",
    "The {Bank of Canada|ORG} lowered its overnight rate to {4.75%|PERCENT}, becoming the first G7 central bank to cut rates.",
    "{Japan|ORG}'s economy avoided a technical recession as revised data showed GDP expanded {0.4%|PERCENT} in {Q4|DATE}.",
    "The yield on the {10-year Treasury note|ORG} surged to {4.7%|PERCENT} following the hot inflation report.",
    "{Eurozone|ORG} inflation slowed to {2.4%|PERCENT} in {April|DATE}, bolstering the case for a {June|DATE} rate cut.",
    "Average hourly earnings increased {0.2%|PERCENT} month-over-month, signaling that wage pressures are easing.",
    "The {Bureau of Labor Statistics|ORG} reported that productivity rose {3.2%|PERCENT} in the first quarter of {2025|DATE}.",
    "{Germany|ORG}'s industrial output dropped {0.4%|PERCENT} in {January|DATE}, raising fears of a protracted downturn.",
    "Consumer confidence in the {US|ORG} fell to {104.7|MONEY} in {March|DATE}, down from a revised {104.8|MONEY} in the prior month.",
    "The {People's Bank of China|ORG} kept the one-year loan prime rate unchanged at {3.45%|PERCENT}.",
    "Housing starts plunged {14.7%|PERCENT} in {March|DATE}, the biggest drop since the pandemic began.",
    "The {Producer Price Index|ORG} rose {0.6%|PERCENT} in {February|DATE}, driven by higher fuel and food costs.",
    "{UK|ORG} inflation dropped to {3.4%|PERCENT} in {February|DATE}, the lowest level in two and a half years.",
    "The trade deficit widened to {$68.9 billion|MONEY} in {February|DATE} as imports outpaced exports.",
    "The {Reserve Bank of Australia|ORG} left the cash rate target at {4.35%|PERCENT} on {Tuesday|DATE}.",
    "Pending home sales rebounded {1.6%|PERCENT} in {February|DATE} despite mortgage rates remaining near {7%|PERCENT}.",
    "The unemployment rate ticked up to {3.9%|PERCENT} in {February|DATE}, hitting a two-year high.",
    "{Saudi Arabia|ORG} announced it would extend its voluntary oil production cut of {1 million bpd|MONEY} through {Q2|DATE}.",
    "Global debt hit a record {$313 trillion|MONEY} in {2024|DATE}, according to the {Institute of International Finance|ORG}.",
    "The {Swiss National Bank|ORG} surprised markets with a rate cut to {1.5%|PERCENT} to curb the franc's strength.",

    # --- BATCH 9: Specialized Ticker/Indicator/Event (30) ---
    "On {Monday|DATE}, {Apple|ORG} ({$AAPL|TICKER}) announced the {acquisition|EVENT} of AI startup {DarwinAI|ORG} to bolster its generative AI capabilities.",
    "The {Bureau of Economic Analysis|ORG} reported that {real gross domestic product|INDICATOR} increased at an annual rate of {3.2%|PERCENT} in {Q4 2025|DATE}.",
    "Shares of {Tesla|ORG} ({TSLA|TICKER}) slid {4%|PERCENT} after the company announced a delay in its upcoming robotaxi unveiling.",
    "The {Consumer Price Index|INDICATOR} rose {0.4%|PERCENT} in {September|DATE}, indicating that inflation remains persistent.",
    "{Microsoft|ORG} ({$MSFT|TICKER}) completed its {$69 billion|MONEY} {merger|EVENT} with {Activision Blizzard|ORG}, ending a lengthy regulatory battle.",
    "Traders are awaiting the {non-farm payrolls|INDICATOR} report on {Friday|DATE} to gauge the health of the labor market.",
    "{Reddit|ORG} officially filed for an {IPO|EVENT} under the ticker symbol {$RDDT|TICKER}, targeting a valuation of over {$6 billion|MONEY}.",
    "The {European Central Bank|ORG} is closely monitoring the {Eurozone HICP inflation rate|INDICATOR}, which held steady at {2.6%|PERCENT}.",
    "{Nvidia|ORG} ({NVDA|TICKER}) overtook {Alphabet|ORG} ({GOOGL|TICKER}) in market cap following a blowout earnings report.",
    "Venture capital firm {Andreessen Horowitz|ORG} led a {$100 million|MONEY} {Series B funding|EVENT} round for crypto startup {EigenLayer|ORG}.",
    "The {unemployment rate|INDICATOR} ticked up to {3.9%|PERCENT} in {February|DATE}, reaching its highest level in two years.",
    "{Broadcom|ORG} ({AVGO|TICKER}) shares rose after completing the {spinoff|EVENT} of its end-user computing unit.",
    "Economists predict the {Personal Consumption Expenditures (PCE) price index|INDICATOR} will show cooling inflation next month.",
    "{Salesforce|ORG} ({CRM|TICKER}) announced a definitive agreement for the {acquisition|EVENT} of data management firm {Informatica|ORG}.",
    "{Japan|ORG}'s {Nikkei 225|TICKER} index crossed the {40,000|MONEY} mark for the first time in history on {Monday|DATE}.",
    "The {Federal Reserve|ORG} pays close attention to the {Employment Cost Index|INDICATOR} to watch for wage-push inflation.",
    "{Amazon|ORG} ({$AMZN|TICKER}) abandoned its planned {$1.4 billion|MONEY} {acquisition|EVENT} of {iRobot|ORG} due to EU opposition.",
    "{Bitcoin|ORG} ({BTC-USD|TICKER}) rallied past {$70,000|MONEY} ahead of the upcoming 'halving' {event|EVENT} in {April|DATE}.",
    "The {Institute for Supply Management|ORG}'s {Manufacturing PMI|INDICATOR} fell to {47.8%|PERCENT} in {February|DATE}, indicating contraction.",
    "{Disney|ORG} ({DIS|TICKER}) defeated activist investors in a proxy battle regarding board seats at the annual shareholder meeting.",
    "{Stripe|ORG} managed to raise {$6.5 billion|MONEY} in a {Series I funding|EVENT} round at a {$50 billion|MONEY} valuation.",
    "{China|ORG}'s {producer price index (PPI)|INDICATOR} fell {2.7%|PERCENT} year-on-year, signaling persistent deflationary pressure.",
    "{Goldman Sachs|ORG} ({GS|TICKER}) acted as the lead advisor on the {$53 billion|MONEY} {merger|EVENT} between {Chevron|ORG} and {Hess|ORG}.",
    "US {retail sales|INDICATOR} rebounded {0.6%|PERCENT} in {March|DATE}, suggesting consumers remain resilient.",
    "{Meta Platforms|ORG} ({META|TICKER}) declared its first-ever quarterly dividend of {$0.50|MONEY} per share.",
    "The {Bank of England|ORG} is concerned that sticky {services inflation|INDICATOR} will prevent early rate cuts in {2026|DATE}.",
    "Cybersecurity firm {Rubrik|ORG} filed for an {IPO|EVENT} on the {NYSE|ORG} under the ticker {$RBRK|TICKER}.",
    "{Housing starts|INDICATOR} plunged {14.7%|PERCENT} last month, the biggest drop since the pandemic began.",
    "{Exxon Mobil|ORG} ({XOM|TICKER}) completed its {acquisition|EVENT} of {Pioneer Natural Resources|ORG} in an all-stock deal.",
    "The {University of Michigan consumer sentiment index|INDICATOR} fell slightly to {76.5|MONEY} in mid-{March|DATE}.",

    # --- BATCH 10: The Equalizer (60 High Density) ---
    "Market leaders {NVDA|TICKER}, {AMD|TICKER}, and {INTC|TICKER} all saw heavy trading volume today.",
    "The correlation between {$BTC-USD|TICKER} and {$ETH-USD|TICKER} has decoupled from the {Nasdaq 100|TICKER}.",
    "Investors are hedging via {GLD|TICKER} (Gold) and {SLV|TICKER} (Silver) ETFs amid volatility.",
    "In Tokyo, {7203.T|TICKER} (Toyota) and {6758.T|TICKER} (Sony) dragged the {Nikkei 225|TICKER} lower.",
    "The spread between the {2-year Treasury yield|INDICATOR} and the {10-year Treasury yield|INDICATOR} inverted further.",
    "Upcoming data on {initial jobless claims|INDICATOR} and {continuing claims|INDICATOR} will guide the Fed.",
    "{GDP growth|INDICATOR} slowed, but {industrial production|INDICATOR} surprised to the upside.",
    "The {acquisition|EVENT} of {Ansys|ORG} by {Synopsys|ORG} is the largest {M&A|EVENT} deal this year.",
    "{Stripe|ORG} is preparing for a direct listing {IPO|EVENT} rather than a traditional {initial public offering|EVENT}.",
    "{Alibaba|ORG} canceled the {spinoff|EVENT} of its Cloud Intelligence Group, impacting {$BABA|TICKER}.",
    "High-yield bonds {HYG|TICKER} are underperforming investment-grade corporate bonds {LQD|TICKER}.",
    "{Consumer confidence|INDICATOR} dipped to 102.0, contrasting with strong {retail sales|INDICATOR} data.",
    "The {merger|EVENT} between {Kroger|ORG} ({KR|TICKER}) and {Albertsons|ORG} ({ACI|TICKER}) faces antitrust roadblocks.",
    "{Exxon|ORG} ({XOM|TICKER}) completed its {buyout|EVENT} of {Pioneer|ORG} ({PXD|TICKER}).",
    "Look for the {ISM Manufacturing PMI|INDICATOR} and {Services PMI|INDICATOR} to define the trend.",
    "{Reliance|ORG} ({RELIANCE.NS|TICKER}) and {HDFC Bank|ORG} ({HDFCBANK.NS|TICKER}) lifted the {Nifty 50|TICKER} index.",
    "The {Core PCE Price Index|INDICATOR} is preferred over the {CPI|INDICATOR} for inflation tracking.",
    "A {stock split|EVENT} for {Nvidia|ORG} ({NVDA|TICKER}) could boost retail participation.",
    "{Super Micro Computer|ORG} ({SMCI|TICKER}) joined the {S&P 500|TICKER} index following its rally.",
    "The {hostile takeover|EVENT} bid for {U.S. Steel|ORG} ({X|TICKER}) by {Nippon Steel|ORG} sparked political debate.",
    "{Housing starts|INDICATOR} and {building permits|INDICATOR} both fell, signaling a construction slowdown.",
    "{German Factory Orders|INDICATOR} dropped, weighing on the {DAX|TICKER} index.",
    "Crypto exchange {Coinbase|ORG} ({COIN|TICKER}) benefited from the new {Bitcoin ETF|EVENT} approvals.",
    "The {Series A funding|EVENT} for {Mistral AI|ORG} valued the company at €2 billion.",
    "{Palantir|ORG} ({PLTR|TICKER}) soared after securing a new government contract.",
    "Traders are watching the {VIX|TICKER} volatility index as {put/call ratios|INDICATOR} hit extremes.",
    "{Oracle|ORG} ({ORCL|TICKER}) announced a {debt offering|EVENT} to finance its data center expansion.",
    "{Existing home sales|INDICATOR} rose, but {pending home sales|INDICATOR} remained flat.",
    "{T-Mobile|ORG} ({TMUS|TICKER}) announced a {$19 billion|MONEY} {share buyback|EVENT} program.",
    "The {bankruptcy filing|EVENT} by {WeWork|ORG} caused its stock ({WE|TICKER}) to be delisted.",
    "{China|ORG}'s {exports|INDICATOR} grew, but {imports|INDICATOR} shrank, widening the trade surplus.",
    "{SoftBank|ORG} ({9984.T|TICKER}) is targeting a {listing|EVENT} for its chip unit {Arm|ORG} ({ARM|TICKER}).",
    "Investors pivoted from growth stocks {QQQ|TICKER} to value stocks {VTV|TICKER}.",
    "{Producer Prices (PPI)|INDICATOR} came in hotter than expected compared to {Consumer Prices (CPI)|INDICATOR}.",
    "The {private equity buyout|EVENT} of {DocuSign|ORG} ({DOCU|TICKER}) is rumored to be finalized soon.",
    "{Pfizer|ORG} ({PFE|TICKER}) completed the {acquisition|EVENT} of {Seagen|ORG} ({SGEN|TICKER}).",
    "{UK GDP|INDICATOR} contracted, pushing the {FTSE 100|TICKER} into negative territory.",
    "{Meta|ORG} ({META|TICKER}) declared a dividend, a rare {financial event|EVENT} for a tech giant.",
    "{Snowflake|ORG} ({SNOW|TICKER}) appointed a new CEO, causing volatility in the stock.",
    "{Tesla|ORG} ({TSLA|TICKER}) faces competition from {BYD|ORG} ({1211.HK|TICKER}) in China.",
    "The {Eurozone PMI|INDICATOR} and {UK PMI|INDICATOR} diverged significantly this month.",
    "{Shein|ORG} filed confidential papers for a US {IPO|EVENT}.",
    "{Goldman Sachs|ORG} ({GS|TICKER}) and {Morgan Stanley|ORG} ({MS|TICKER}) led the {underwriting|EVENT}.",
    "The {Labor Force Participation Rate|INDICATOR} is a key metric alongside the {Unemployment Rate|INDICATOR}.",
    "{Disney|ORG} ({DIS|TICKER}) won the proxy vote, avoiding a board {shakeup|EVENT}.",
    "{Utilities|TICKER} (XLU) and {Consumer Staples|TICKER} (XLP) are acting as defensive plays.",
    "{Japan|ORG}'s {Tankan Large Manufacturers Index|INDICATOR} improved in Q4.",
    "{Broadcom|ORG} ({AVGO|TICKER}) is a top holding in many {semiconductor ETFs|TICKER} like {SOXX|TICKER}.",
    "The {Series B round|EVENT} for {Perplexity AI|ORG} attracted {Nvidia|ORG} ({NVDA|TICKER}) as an investor.",
    "{Crude Oil Inventories|INDICATOR} rose, pushing oil prices down.",
    "{MicroStrategy|ORG} ({MSTR|TICKER}) bought more Bitcoin, acting as a proxy for the crypto asset.",
    "{GameStop|ORG} ({GME|TICKER}) and {AMC|ORG} ({AMC|TICKER}) saw a resurgence in meme stock activity.",
    "The {merger|EVENT} of {Zee Entertainment|ORG} ({ZEEL.NS|TICKER}) and {Sony India|ORG} was called off.",
    "{Fed Chair Powell|PER} discussed the {PCE deflator|INDICATOR} during his testimony.",
    "{Visa|ORG} ({V|TICKER}) and {Mastercard|ORG} ({MA|TICKER}) announced a settlement regarding swipe fees.",
    "{UnitedHealth|ORG} ({UNH|TICKER}) fell after the {cyberattack|EVENT} on its subsidiary.",
    "{Inflation expectations|INDICATOR} have anchored near 3%, according to the {Michigan Survey|INDICATOR}.",
    "{Dell|ORG} ({DELL|TICKER}) surged on AI server demand, joining the {AI rally|EVENT}.",
    "{Rivian|ORG} ({RIVN|TICKER}) paused the construction of its Georgia plant to save cash.",
    "The {Federal Funds Rate|INDICATOR} is currently restrictive, affecting {mortgage rates|INDICATOR}."
]

# ==========================================
# PARSER: CONVERT TO SPACY JSON FORMAT
# ==========================================
def convert_to_spacy(data_list):
    training_data = []
    # Regex to capture {Text|LABEL}
    pattern = re.compile(r"\{(.*?)\|([A-Z]+)\}")
    
    for line in data_list:
        clean_text = ""
        entities = []
        cursor = 0
        last_match_end = 0
        
        for match in pattern.finditer(line):
            # Append text before the tag
            pre_text = line[last_match_end:match.start()]
            clean_text += pre_text
            cursor += len(pre_text)
            
            # Capture entity and label
            entity_text = match.group(1)
            label = match.group(2)
            
            # Store offsets
            start_char = cursor
            end_char = cursor + len(entity_text)
            entities.append((start_char, end_char, label))
            
            # Append entity text to clean string
            clean_text += entity_text
            cursor += len(entity_text)
            last_match_end = match.end()
            
        # Append remaining text
        clean_text += line[last_match_end:]
        
        # Add to list if entities exist
        if entities:
            training_data.append((clean_text, {"entities": entities}))
            
    return training_data

# ==========================================
# EXECUTION
# ==========================================
final_data = convert_to_spacy(raw_data)
random.shuffle(final_data)

# Split 80/20
split = int(len(final_data) * 0.8)
train = final_data[:split]
dev = final_data[split:]

print(f"Successfully processed {len(final_data)} examples.")
print(f"Training Set: {len(train)}")
print(f"Development Set: {len(dev)}")

# Save files
with open("train_financial_ner.json", "w") as f:
    json.dump(train, f, indent=2)
    
with open("dev_financial_ner.json", "w") as f:
    json.dump(dev, f, indent=2)
    
print("Files 'train_financial_ner.json' and 'dev_financial_ner.json' have been created.")