# Matcher dry-run — adversarial review sheet

**Task for the reviewer: find the site that should NOT have matched.**

298 sites across 24 traces (~1788 words). Every
matched span is shown as ⟦span⟧ with surrounding context. For each site
ask: would swapping the span for any listed candidate change ANY of —
propositions, dependency structure, hedging, which intermediates are
explicit, step granularity/schedule? If yes for even one candidate, the
site is bad and must be dispositioned (matcher fix vs. table amendment)
per CLAUDE.md Step 3.

## tier_a_01_connectives — 31 sites

**tier_a_01#1** `01_multiplication_basic.txt` [97:99] set `inferential`
  candidates: `so | thus | therefore | hence`
> …to compute 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, ⟦so⟧ 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 2…

**tier_a_01#2** `01_multiplication_basic.txt` [201:205] set `inferential`
  candidates: `Thus | Therefore | Hence | So`
> …760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n\n⟦Thus⟧, the product is 4042.\n\nANSWER: 4042\n

**tier_a_01#3** `02_multiplication_ordinals.txt` [258:267] set `inferential`
  candidates: `Therefore | Thus | Hence | So`
> …4 * 12 = 2808.\n\nThird, add the two partial results. The total is 117000 + 2808 = 119808.\n\n⟦Therefore⟧ the answer is 119808.\n\nANSWER: 119808\n

**tier_a_01#4** `03_composition_chain.txt` [356:358] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …e reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.\n\n⟦So⟧ the final value is 93.\n\nANSWER: 93\n

**tier_a_01#5** `04_composition_negative.txt` [304:309] set `inferential`
  candidates: `Hence | Thus | Therefore | So`
> …since each step multiplies a\nnegative value by a positive constant and then subtracts 5.\n\n⟦Hence⟧ the result is -56.\n\nANSWER: -56\n

**tier_a_01#6** `05_reachability_arrows.txt` [216:218] set `inferential`
  candidates: `so | thus | therefore | hence`
> …->N1 and N0->D0.\n\nFollow N0->N1. From N1 the only edge is N1->N2. From N2 we have N2->N3, ⟦so⟧ we\nreach the target. The path N0->N1->N2->N3 uses 3 edges.\n\nThe decoy branch through D0 o…

**tier_a_01#7** `05_reachability_arrows.txt` [338:340] set `inferential`
  candidates: `so | thus | therefore | hence`
> … N0->N1->N2->N3 uses 3 edges.\n\nThe decoy branch through D0 only cycles between D0 and D1, ⟦so⟧ it never reaches\nthe target.\n\nTherefore the path exists and has length 3.\n\nANSWER: 3\n

**tier_a_01#8** `05_reachability_arrows.txt` [371:380] set `inferential`
  candidates: `Therefore | Thus | Hence | So`
> …e decoy branch through D0 only cycles between D0 and D1, so it never reaches\nthe target.\n\n⟦Therefore⟧ the path exists and has length 3.\n\nANSWER: 3\n

**tier_a_01#9** `06_reachability_so_that.txt` [353:355] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …m S we reach A and B. From A we reach C. From B we reach\nnothing new. From C we reach T.\n\n⟦So⟧ the path S->A->C->T exists, and it has 3 edges. We chose the ordering so that\nno edge was…

**tier_a_01#10** `07_prose_geometry.txt` [419:423] set `inferential`
  candidates: `Thus | Therefore | Hence | So`
> …ame about reflections changing orientation, but orientation\ndoes not affect side lengths. ⟦Thus⟧, the area is (5 * 12) / 2 = 30.\n\nANSWER: 30\n

**tier_a_01#11** `08_prose_quotes.txt` [244:246] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> … since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that 21 * 4 = 84. ⟦So⟧ the answer follows directly: 7 divides 21 * 4, and\nby the quoted lemma 7 must divide 21 o…

**tier_a_01#12** `09_code_fenced.txt` [224:226] set `inferential`
  candidates: `so | thus | therefore | hence`
> …t touch the seed values\nprint(f"result={thus}")\n```\n\nThe loop maintains two accumulators, ⟦so⟧ the final print shows the tenth term.\nRunning it gives 89.\n\nThus, the tenth Fibonacci num…

**tier_a_01#13** `09_code_fenced.txt` [287:291] set `inferential`
  candidates: `Thus | Therefore | Hence | So`
> …aintains two accumulators, so the final print shows the tenth term.\nRunning it gives 89.\n\n⟦Thus⟧, the tenth Fibonacci number under this indexing is 89.\n\nANSWER: 89\n

**tier_a_01#14** `10_code_inline.txt` [208:210] set `inferential`
  candidates: `so | thus | therefore | hence`
> …tor can't overflow here, because the loop adds at most 97 per\niteration and runs 6 times, ⟦so⟧ the maximum is 582.\n\nTherefore the guard `assert so_far <= 582` always passes.\n\nANSWER: 5…

**tier_a_01#15** `10_code_inline.txt` [232:241] set `inferential`
  candidates: `Therefore | Thus | Hence | So`
> … because the loop adds at most 97 per\niteration and runs 6 times, so the maximum is 582.\n\n⟦Therefore⟧ the guard `assert so_far <= 582` always passes.\n\nANSWER: 582\n

**tier_a_01#16** `11_ranges.txt` [218:220] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …rounding down from\n7.5). Pick offset 2.\n\nNow compute the index: 7 * 3 - 2 = 21 - 2 = 19.\n\n⟦So⟧ the index is 19, which lies outside 5-10, as required.\n\nANSWER: 19\n

**tier_a_01#17** `12_scientific.txt` [248:253] set `inferential`
  candidates: `Hence | Thus | Therefore | So`
> …he error is 2e-4, after two steps 2e-5, and\nafter three steps 2e-6, which is below 1e-5.\n\n⟦Hence⟧ we need 3 iterations.\n\nANSWER: 3\n

**tier_a_01#18** `13_comparative_so.txt` [236:238] set `inferential`
  candidates: `so | thus | therefore | hence`
> …ells us nothing below n = 100. For\nsmall n we compute directly.\n\nAt n = 10 the sum is 55, ⟦so⟧ the direct value is what we report. The gap\nbetween the bound and the truth was so large …

**tier_a_01#19** `14_purpose_so_that.txt` [166:168] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> … 4\ngives x*x + 2*x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\n⟦So⟧ the roots are -3 and 1. We arranged the factorization so that the signs are\nimmediate to …

**tier_a_01#20** `15_conditional_then.txt` [313:317] set `inferential`
  candidates: `Thus | Therefore | Hence | So`
> …d, then the second rule would apply, and\nindeed 49 = 48 + 1 leaves remainder 1 modulo 8.\n\n⟦Thus⟧, the divisibility claim holds for x = 6.\n\nANSWER: yes\n

**tier_a_01#21** `16_enumeration.txt` [307:316] set `inferential`
  candidates: `Therefore | Thus | Hence | So`
> … 2*2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.\n\n⟦Therefore⟧ both methods agree.\n\nANSWER: 4\n

**tier_a_01#22** `17_possessive_its.txt` [294:296] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …t components once. The graph has 3 components,\nand each keeps its size under relabeling.\n\n⟦So⟧ the component count is 3.\n\nANSWER: 3\n

**tier_a_01#23** `18_quoted_dialogue.txt` [330:334] set `inferential`
  candidates: `Thus | Therefore | Hence | So`
> …easoning starts here.\n\nWe need the square root of 144, which is 12, since 12 * 12 = 144.\n\n⟦Thus⟧, the requested value is 12.\n\nANSWER: 12\n

**tier_a_01#24** `20_display_lines.txt` [183:185] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …set would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40\ny = 23.\n\n⟦So⟧ the chain returns to its starting value after one full cycle.\n\nANSWER: 23\n

**tier_a_01#25** `21_markdown_mixed.txt` [251:253] set `inferential`
  candidates: `So | Thus | Therefore | Hence`
> …alue after step 2 is 42.\n\n## Verification\n\nEach step multiplies by 3. Check: 14 * 3 = 42. ⟦So⟧ the table is consistent.\n\nANSWER: 42\n

**tier_a_01#26** `22_hedging.txt` [109:111] set `inferential`
  candidates: `so | thus | therefore | hence`
> …ence is arithmetic, but we should verify rather than\nassume. The differences are 7, 7, 7, ⟦so⟧ it is indeed arithmetic with common\ndifference 7.\n\nPerhaps a closed form helps: a(n) = 4 …

**tier_a_01#27** `22_hedging.txt` [333:335] set `inferential`
  candidates: `so | thus | therefore | hence`
> … be safe, check directly: 4 + 70 = 74. The hedged guess and the direct\ncomputation agree, ⟦so⟧ the answer stands.\n\nANSWER: 74\n

**tier_a_01#28** `23_lets_hortative.txt` [365:367] set `inferential`
  candidates: `so | thus | therefore | hence`
> …10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth power gives the tenth\npower, ⟦so⟧ the check confirms it.\n\nANSWER: 1\n

**tier_a_01#29** `24_kitchen_sink.txt` [151:153] set `inferential`
  candidates: `so | thus | therefore | hence`
> …3, then report\nwhether the result lies in the range 10-200.\n\nIt's a two-step composition, ⟦so⟧ we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 …

**tier_a_01#30** `24_kitchen_sink.txt` [510:515] set `inferential`
  candidates: `Hence | Thus | Therefore | So`
> …ound: 166 <= 200 holds\n\nIf both bounds hold, then the value lies in the range. Both hold. ⟦Hence⟧ the\nanswer is yes, and its verification needed only two comparisons. We can't\nskip the bo…

**tier_a_01#31** `24_kitchen_sink.txt` [764:773] set `inferential`
  candidates: `Therefore | Thus | Hence | So`
> …\ndef h(x):\n    return x*x - 3  # so simple it can't hide a bug\nassert h(h(4)) == 166\n```\n\n⟦Therefore⟧ the final answer is yes.\n\nANSWER: yes\n

## tier_a_02_punctuation — 15 sites

**tier_a_02#1** `01_multiplication_basic.txt` [140:144] set `comma_after_initial_connective`
  candidates: `Now  | Now, `
> …0 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\n⟦Now ⟧add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, the product is 4042.\n\nANSWE…

**tier_a_02#2** `03_composition_chain.txt` [145:149] set `comma_after_initial_connective`
  candidates: `Now  | Now, `
> …h x = 23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\n⟦Now ⟧reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 =…

**tier_a_02#3** `03_composition_chain.txt` [175:181] set `comma_after_initial_connective`
  candidates: `Then,  | Then `
> …(11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\n⟦Then, ⟧apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We red…

**tier_a_02#4** `03_composition_chain.txt` [224:225] set `final_period_on_display_line`
  candidates: `\n | .\n`
> …+ 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97⟦\n⟧Compute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. …

**tier_a_02#5** `03_composition_chain.txt` [293:299] set `comma_after_initial_connective`
  candidates: `Next,  | Next `
> … = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\n⟦Next, ⟧apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.\n\nSo the final value is 93.\n\nANSWER…

**tier_a_02#6** `11_ranges.txt` [169:173] set `comma_after_initial_connective`
  candidates: `Now  | Now, `
> … midpoint of 5-10, which is 7 (integer midpoint, rounding down from\n7.5). Pick offset 2.\n\n⟦Now ⟧compute the index: 7 * 3 - 2 = 21 - 2 = 19.\n\nSo the index is 19, which lies outside 5-10, …

**tier_a_02#7** `15_conditional_then.txt` [121:127] set `comma_after_initial_connective`
  candidates: `Then,  | Then `
> …ible by 4. If x is odd, then x*x leaves\nremainder 1 modulo 8.\n\nOur x is 6, which is even. ⟦Then, ⟧by the first rule, 36 is divisible by 4.\nCheck: 36 = 4 * 9.\n\nIf we had started from x = 7 …

**tier_a_02#8** `16_enumeration.txt` [160:166] set `comma_after_initial_connective`
  candidates: `Next,  | Next `
> … keep only the perfect squares among them: 1, 4, 9, 36.\n\nThird, count them. There are 4.\n\n⟦Next, ⟧we double-check by the exponent formula. Since 36 = 2*2 * 3*3, a divisor\nis a square iff b…

**tier_a_02#9** `20_display_lines.txt` [37:38] set `final_period_on_display_line`
  candidates: `\n | .\n`
> Track the value line by line.\n\nx = 23⟦\n⟧f1(x) = (11*23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but the…

**tier_a_02#10** `20_display_lines.txt` [64:65] set `final_period_on_display_line`
  candidates: `\n | .\n`
> Track the value line by line.\n\nx = 23\nf1(x) = (11*23 + 4) mod 97⟦\n⟧f1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\npro…

**tier_a_02#11** `20_display_lines.txt` [75:77] set `final_period_on_display_line`
  candidates: `.\n | \n`
> Track the value line by line.\n\nx = 23\nf1(x) = (11*23 + 4) mod 97\nf1(x) = 63⟦.\n⟧\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 6…

**tier_a_02#12** `20_display_lines.txt` [173:174] set `final_period_on_display_line`
  candidates: `\n | .\n`
> …ng the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40⟦\n⟧y = 23.\n\nSo the chain returns to its starting value after one full cycle.\n\nANSWER: 23\n

**tier_a_02#13** `20_display_lines.txt` [180:182] set `final_period_on_display_line`
  candidates: `.\n | \n`
> …offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40\ny = 23⟦.\n⟧\nSo the chain returns to its starting value after one full cycle.\n\nANSWER: 23\n

**tier_a_02#14** `24_kitchen_sink.txt` [200:201] set `final_period_on_display_line`
  candidates: `\n | .\n`
> …ge 10-200.\n\nIt's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3⟦\n⟧h(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positive, and…

**tier_a_02#15** `24_kitchen_sink.txt` [210:212] set `final_period_on_display_line`
  candidates: `.\n | \n`
> …\n\nIt's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13⟦.\n⟧\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positive, and the proble…

## tier_a_03_discourse_markers — 8 sites

**tier_a_03#1** `01_multiplication_basic.txt` [28:34] set `initiation`
  candidates: `First, | To start, | To begin,`
> I need to compute 47 * 86.\n\n⟦First,⟧ break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute…

**tier_a_03#2** `04_composition_negative.txt` [168:177] set `attention`
  candidates: `Note that | Observe that | Notice that`
> …= 3*(-4) - 5 = -12 - 5 = -17.\n\nSecond application: g(-17) = 3*(-17) - 5 = -51 - 5 = -56.\n\n⟦Note that⟧ the sign stays negative throughout, since each step multiplies a\nnegative value by a posi…

**tier_a_03#3** `07_prose_geometry.txt` [244:259] set `recap`
  candidates: `In other words, | That is,`
> …ition.\n\nThe triangle keeps its right angle under scaling, since scaling preserves\nangles. ⟦In other words,⟧ every similar triangle is also a right triangle.\n\nWe cannot say the same about reflection…

**tier_a_03#4** `08_prose_quotes.txt` [131:140] set `attention`
  candidates: `Note that | Observe that | Notice that`
> … a prime divides a product, then it\ndivides one of the factors." This is Euclid's lemma.\n\n⟦Note that⟧ 7 divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that…

**tier_a_03#5** `08_prose_quotes.txt` [218:230] set `attention`
  candidates: `Observe that | Note that | Notice that`
> ….\n\nNote that 7 divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\n⟦Observe that⟧ 21 * 4 = 84. So the answer follows directly: 7 divides 21 * 4, and\nby the quoted lemma 7 …

**tier_a_03#6** `18_quoted_dialogue.txt` [143:152] set `attention`
  candidates: `Note that | Observe that | Notice that`
> …s are positive," and the\nsecond card reads "Therefore you may take square roots freely."\n\n⟦Note that⟧ the instructions quoted above are part of the puzzle text, not our\nreasoning. Our own rea…

**tier_a_03#7** `24_kitchen_sink.txt` [0:6] set `initiation`
  candidates: `First, | To start, | To begin,`
> ⟦First,⟧ restate the task: evaluate h(h(4)) where h(x) = x*x - 3, then report\nwhether the result l…

**tier_a_03#8** `24_kitchen_sink.txt` [261:270] set `attention`
  candidates: `Note that | Observe that | Notice that`
> …\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\n⟦Note that⟧ 166 is positive, and the problem said "report whether the result\nlies in the range," so t…

## tier_a_04_contractions — 16 sites

**tier_a_04#1** `06_reachability_so_that.txt` [171:177] set `cant`
  candidates: `cannot | can't`
> …dex. This works because the graph is acyclic.\n\nIf a vertex has no outgoing edges, then it ⟦cannot⟧ lie on any path to the target\nunless it is the target itself.\n\nScan the frontier. From S …

**tier_a_04#2** `06_reachability_so_that.txt` [215:220] set `its`
  candidates: `it is | it's`
> ….\n\nIf a vertex has no outgoing edges, then it cannot lie on any path to the target\nunless ⟦it is⟧ the target itself.\n\nScan the frontier. From S we reach A and B. From A we reach C. From B…

**tier_a_04#3** `07_prose_geometry.txt` [48:52] set `its`
  candidates: `It's | It is`
> Consider the triangle with sides 5, 12, and 13. ⟦It's⟧ a right triangle, because\n5*5 + 12*12 = 25 + 144 = 169 = 13*13, which is exactly the Pyth…

**tier_a_04#4** `07_prose_geometry.txt` [313:319] set `cant`
  candidates: `cannot | can't`
> …ng preserves\nangles. In other words, every similar triangle is also a right triangle.\n\nWe ⟦cannot⟧ say the same about reflections changing orientation, but orientation\ndoes not affect side…

**tier_a_04#5** `07_prose_geometry.txt` [389:397] set `doesnt`
  candidates: `does not | doesn't`
> …triangle.\n\nWe cannot say the same about reflections changing orientation, but orientation\n⟦does not⟧ affect side lengths. Thus, the area is (5 * 12) / 2 = 30.\n\nANSWER: 30\n

**tier_a_04#6** `08_prose_quotes.txt` [418:425] set `thats`
  candidates: `that is | that's`
> …ide 21 or divide 4. Indeed 21 = 7 * 3.\n\nThe hint said "Thus, use the lemma directly," and ⟦that is⟧ what we did.\n\nANSWER: yes\n

**tier_a_04#7** `10_code_inline.txt` [122:127] set `cant`
  candidates: `can't | cannot`
> … before the run, and keep `so_far=0` as the\naccumulator's initial value.\n\nThe accumulator ⟦can't⟧ overflow here, because the loop adds at most 97 per\niteration and runs 6 times, so the ma…

**tier_a_04#8** `17_possessive_its.txt` [73:79] set `cant`
  candidates: `cannot | can't`
> The graph keeps its edge set fixed while we relabel vertices. Relabeling\n⟦cannot⟧ change connectivity, because an edge exists after relabeling iff its\npreimage existed bef…

**tier_a_04#9** `17_possessive_its.txt` [175:179] set `its`
  candidates: `It's | It is`
> …e connectivity, because an edge exists after relabeling iff its\npreimage existed before.\n\n⟦It's⟧ therefore enough to count components once. The graph has 3 components,\nand each keeps its…

**tier_a_04#10** `22_hedging.txt` [112:117] set `its`
  candidates: `it is | it's`
> …e is arithmetic, but we should verify rather than\nassume. The differences are 7, 7, 7, so ⟦it is⟧ indeed arithmetic with common\ndifference 7.\n\nPerhaps a closed form helps: a(n) = 4 + 7*n.…

**tier_a_04#11** `23_lets_hortative.txt` [0:5] set `lets`
  candidates: `Let's | Let us`
> ⟦Let's⟧ compute the residue of 2 to the power 10 modulo 11.\n\nFermat's little theorem lets us redu…

**tier_a_04#12** `23_lets_hortative.txt` [185:191] set `isnt`
  candidates: `is not | isn't`
> …ce the exponent: 2 to the power 10 is\ncongruent to 1 modulo 11, because 11 is prime and 2 ⟦is not⟧ divisible by 11.\n\nLet us double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, th…

**tier_a_04#13** `23_lets_hortative.txt` [210:216] set `lets`
  candidates: `Let us | Let's`
> … power 10 is\ncongruent to 1 modulo 11, because 11 is prime and 2 is not divisible by 11.\n\n⟦Let us⟧ double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 m…

**tier_a_04#14** `24_kitchen_sink.txt` [122:126] set `its`
  candidates: `It's | It is`
> …e h(h(4)) where h(x) = x*x - 3, then report\nwhether the result lies in the range 10-200.\n\n⟦It's⟧ a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOut…

**tier_a_04#15** `24_kitchen_sink.txt` [359:366] set `thats`
  candidates: `that is | that's`
> …t 166 is positive, and the problem said "report whether the result\nlies in the range," so ⟦that is⟧ what we do:\n\n- lower bound: 166 >= 10 holds\n- upper bound: 166 <= 200 holds\n\nIf both boun…

**tier_a_04#16** `24_kitchen_sink.txt` [588:593] set `cant`
  candidates: `can't | cannot`
> … Both hold. Hence the\nanswer is yes, and its verification needed only two comparisons. We ⟦can't⟧\nskip the bounds check, since 13*13 might plausibly have exceeded 200.\n\n```python\ndef h(x)…

## tier_a_05_whitespace — 89 sites

**tier_a_05#1** `01_multiplication_basic.txt` [26:28] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> I need to compute 47 * 86.⟦\n\n⟧First, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nC…

**tier_a_05#2** `01_multiplication_basic.txt` [56:58] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> I need to compute 47 * 86.\n\nFirst, break 86 into 80 + 6.⟦\n\n⟧Compute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add …

**tier_a_05#3** `01_multiplication_basic.txt` [115:117] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> ….\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.⟦\n\n⟧Compute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, …

**tier_a_05#4** `01_multiplication_basic.txt` [138:140] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.⟦\n\n⟧Now add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, the product is 4042.\n\nA…

**tier_a_05#5** `01_multiplication_basic.txt` [199:201] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.⟦\n\n⟧Thus, the product is 4042.\n\nANSWER: 4042\n

**tier_a_05#6** `01_multiplication_basic.txt` [227:229] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> ….\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, the product is 4042.⟦\n\n⟧ANSWER: 4042\n

**tier_a_05#7** `02_multiplication_ordinals.txt` [50:52] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> We want 234 * 512. I will proceed in three stages.⟦\n\n⟧First, multiply 234 by 500. Since 234 * 5 = 1170, we get 234 * 500 = 117000.\n\nSecond, mult…

**tier_a_05#8** `02_multiplication_ordinals.txt` [128:130] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …hree stages.\n\nFirst, multiply 234 by 500. Since 234 * 5 = 1170, we get 234 * 500 = 117000.⟦\n\n⟧Second, multiply 234 by 12. We have 234 * 12 = 2808.\n\nThird, add the two partial results. …

**tier_a_05#9** `02_multiplication_ordinals.txt` [182:184] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …5 = 1170, we get 234 * 500 = 117000.\n\nSecond, multiply 234 by 12. We have 234 * 12 = 2808.⟦\n\n⟧Third, add the two partial results. The total is 117000 + 2808 = 119808.\n\nTherefore the an…

**tier_a_05#10** `02_multiplication_ordinals.txt` [256:258] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …234 * 12 = 2808.\n\nThird, add the two partial results. The total is 117000 + 2808 = 119808.⟦\n\n⟧Therefore the answer is 119808.\n\nANSWER: 119808\n

**tier_a_05#11** `02_multiplication_ordinals.txt` [289:291] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …two partial results. The total is 117000 + 2808 = 119808.\n\nTherefore the answer is 119808.⟦\n\n⟧ANSWER: 119808\n

**tier_a_05#12** `03_composition_chain.txt` [64:66] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> We evaluate the chain from the inside out, starting with x = 23.⟦\n\n⟧Apply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce:…

**tier_a_05#13** `03_composition_chain.txt` [173:175] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …= (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.⟦\n\n⟧Then, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. …

**tier_a_05#14** `03_composition_chain.txt` [291:293] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …3) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.⟦\n\n⟧Next, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.\n\nSo the final value is 93.\n\n…

**tier_a_05#15** `03_composition_chain.txt` [354:356] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.⟦\n\n⟧So the final value is 93.\n\nANSWER: 93\n

**tier_a_05#16** `03_composition_chain.txt` [381:383] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.\n\nSo the final value is 93.⟦\n\n⟧ANSWER: 93\n

**tier_a_05#17** `04_composition_negative.txt` [51:53] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> The map is g(x) = 3*x - 5, applied twice to x = -4.⟦\n\n⟧First application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.\n\nSecond application: g(-17) = 3*(-1…

**tier_a_05#18** `04_composition_negative.txt` [107:109] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … 3*x - 5, applied twice to x = -4.\n\nFirst application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.⟦\n\n⟧Second application: g(-17) = 3*(-17) - 5 = -51 - 5 = -56.\n\nNote that the sign stays negati…

**tier_a_05#19** `04_composition_negative.txt` [166:168] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …) = 3*(-4) - 5 = -12 - 5 = -17.\n\nSecond application: g(-17) = 3*(-17) - 5 = -51 - 5 = -56.⟦\n\n⟧Note that the sign stays negative throughout, since each step multiplies a\nnegative value …

**tier_a_05#20** `04_composition_negative.txt` [302:304] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …, since each step multiplies a\nnegative value by a positive constant and then subtracts 5.⟦\n\n⟧Hence the result is -56.\n\nANSWER: -56\n

**tier_a_05#21** `04_composition_negative.txt` [328:330] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …es a\nnegative value by a positive constant and then subtracts 5.\n\nHence the result is -56.⟦\n\n⟧ANSWER: -56\n

**tier_a_05#22** `05_reachability_arrows.txt` [54:56] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> Edges: N0->N1, N1->N2, D0->D1, N2->N3, D1->D0, N0->D0.⟦\n\n⟧Is there a path from N0 to N3?\n\nStart at N0. Its outgoing edges are N0->N1 and N0->D0.\n\nFo…

**tier_a_05#23** `05_reachability_arrows.txt` [86:88] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> Edges: N0->N1, N1->N2, D0->D1, N2->N3, D1->D0, N0->D0.\n\nIs there a path from N0 to N3?⟦\n\n⟧Start at N0. Its outgoing edges are N0->N1 and N0->D0.\n\nFollow N0->N1. From N1 the only ed…

**tier_a_05#24** `05_reachability_arrows.txt` [142:144] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …0.\n\nIs there a path from N0 to N3?\n\nStart at N0. Its outgoing edges are N0->N1 and N0->D0.⟦\n\n⟧Follow N0->N1. From N1 the only edge is N1->N2. From N2 we have N2->N3, so we\nreach the ta…

**tier_a_05#25** `05_reachability_arrows.txt` [277:279] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …>N2. From N2 we have N2->N3, so we\nreach the target. The path N0->N1->N2->N3 uses 3 edges.⟦\n\n⟧The decoy branch through D0 only cycles between D0 and D1, so it never reaches\nthe target.…

**tier_a_05#26** `05_reachability_arrows.txt` [369:371] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …The decoy branch through D0 only cycles between D0 and D1, so it never reaches\nthe target.⟦\n\n⟧Therefore the path exists and has length 3.\n\nANSWER: 3\n

**tier_a_05#27** `05_reachability_arrows.txt` [414:416] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …en D0 and D1, so it never reaches\nthe target.\n\nTherefore the path exists and has length 3.⟦\n\n⟧ANSWER: 3\n

**tier_a_05#28** `06_reachability_so_that.txt` [126:128] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …edge points from a lower index to a higher\nindex. This works because the graph is acyclic.⟦\n\n⟧If a vertex has no outgoing edges, then it cannot lie on any path to the target\nunless it …

**tier_a_05#29** `06_reachability_so_that.txt` [239:241] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …tgoing edges, then it cannot lie on any path to the target\nunless it is the target itself.⟦\n\n⟧Scan the frontier. From S we reach A and B. From A we reach C. From B we reach\nnothing new…

**tier_a_05#30** `06_reachability_so_that.txt` [351:353] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …rom S we reach A and B. From A we reach C. From B we reach\nnothing new. From C we reach T.⟦\n\n⟧So the path S->A->C->T exists, and it has 3 edges. We chose the ordering so that\nno edge w…

**tier_a_05#31** `06_reachability_so_that.txt` [466:468] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …exists, and it has 3 edges. We chose the ordering so that\nno edge was ever examined twice.⟦\n\n⟧ANSWER: 3\n

**tier_a_05#32** `07_prose_geometry.txt` [160:162] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … because\n5*5 + 12*12 = 25 + 144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.⟦\n\n⟧The triangle keeps its right angle under scaling, since scaling preserves\nangles. In other…

**tier_a_05#33** `07_prose_geometry.txt` [308:310] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …scaling preserves\nangles. In other words, every similar triangle is also a right triangle.⟦\n\n⟧We cannot say the same about reflections changing orientation, but orientation\ndoes not af…

**tier_a_05#34** `07_prose_geometry.txt` [455:457] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …tation, but orientation\ndoes not affect side lengths. Thus, the area is (5 * 12) / 2 = 30.⟦\n\n⟧ANSWER: 30\n

**tier_a_05#35** `08_prose_quotes.txt` [129:131] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …If a prime divides a product, then it\ndivides one of the factors." This is Euclid's lemma.⟦\n\n⟧Note that 7 divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObs…

**tier_a_05#36** `08_prose_quotes.txt` [216:218] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ma.\n\nNote that 7 divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.⟦\n\n⟧Observe that 21 * 4 = 84. So the answer follows directly: 7 divides 21 * 4, and\nby the quo…

**tier_a_05#37** `08_prose_quotes.txt` [366:368] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …7 divides 21 * 4, and\nby the quoted lemma 7 must divide 21 or divide 4. Indeed 21 = 7 * 3.⟦\n\n⟧The hint said "Thus, use the lemma directly," and that is what we did.\n\nANSWER: yes\n

**tier_a_05#38** `08_prose_quotes.txt` [438:440] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …Indeed 21 = 7 * 3.\n\nThe hint said "Thus, use the lemma directly," and that is what we did.⟦\n\n⟧ANSWER: yes\n

**tier_a_05#39** `09_code_fenced.txt` [285:287] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … maintains two accumulators, so the final print shows the tenth term.\nRunning it gives 89.⟦\n\n⟧Thus, the tenth Fibonacci number under this indexing is 89.\n\nANSWER: 89\n

**tier_a_05#40** `09_code_fenced.txt` [346:348] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …th term.\nRunning it gives 89.\n\nThus, the tenth Fibonacci number under this indexing is 89.⟦\n\n⟧ANSWER: 89\n

**tier_a_05#41** `10_code_inline.txt` [104:106] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …dont_retry = True` before the run, and keep `so_far=0` as the\naccumulator's initial value.⟦\n\n⟧The accumulator can't overflow here, because the loop adds at most 97 per\niteration and ru…

**tier_a_05#42** `10_code_inline.txt` [230:232] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …e, because the loop adds at most 97 per\niteration and runs 6 times, so the maximum is 582.⟦\n\n⟧Therefore the guard `assert so_far <= 582` always passes.\n\nANSWER: 582\n

**tier_a_05#43** `10_code_inline.txt` [289:291] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …6 times, so the maximum is 582.\n\nTherefore the guard `assert so_far <= 582` always passes.⟦\n\n⟧ANSWER: 582\n

**tier_a_05#44** `11_ranges.txt` [69:71] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> The seed must lie in the range 5-10, and the offset in the range 1-3.⟦\n\n⟧Pick the midpoint of 5-10, which is 7 (integer midpoint, rounding down from\n7.5). Pick off…

**tier_a_05#45** `11_ranges.txt` [167:169] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …he midpoint of 5-10, which is 7 (integer midpoint, rounding down from\n7.5). Pick offset 2.⟦\n\n⟧Now compute the index: 7 * 3 - 2 = 21 - 2 = 19.\n\nSo the index is 19, which lies outside 5-…

**tier_a_05#46** `11_ranges.txt` [216:218] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …, rounding down from\n7.5). Pick offset 2.\n\nNow compute the index: 7 * 3 - 2 = 21 - 2 = 19.⟦\n\n⟧So the index is 19, which lies outside 5-10, as required.\n\nANSWER: 19\n

**tier_a_05#47** `11_ranges.txt` [275:277] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …index: 7 * 3 - 2 = 21 - 2 = 19.\n\nSo the index is 19, which lies outside 5-10, as required.⟦\n\n⟧ANSWER: 19\n

**tier_a_05#48** `12_scientific.txt` [48:50] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> The tolerance is 1e-5 and the step size is 2e-3.⟦\n\n⟧Each iteration reduces the error by a factor of 10, starting from an error of\nroughly 2e-3…

**tier_a_05#49** `12_scientific.txt` [246:248] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … the error is 2e-4, after two steps 2e-5, and\nafter three steps 2e-6, which is below 1e-5.⟦\n\n⟧Hence we need 3 iterations.\n\nANSWER: 3\n

**tier_a_05#50** `12_scientific.txt` [275:277] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … steps 2e-5, and\nafter three steps 2e-6, which is below 1e-5.\n\nHence we need 3 iterations.⟦\n\n⟧ANSWER: 3\n

**tier_a_05#51** `13_comparative_so.txt` [102:104] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …erm grows so much faster than the first that we can ignore the\nfirst entirely for large n.⟦\n\n⟧The bound we derived is so loose that it tells us nothing below n = 100. For\nsmall n we co…

**tier_a_05#52** `13_comparative_so.txt` [209:211] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …rived is so loose that it tells us nothing below n = 100. For\nsmall n we compute directly.⟦\n\n⟧At n = 10 the sum is 55, so the direct value is what we report. The gap\nbetween the bound …

**tier_a_05#53** `13_comparative_so.txt` [368:370] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … gap\nbetween the bound and the truth was so large that only direct computation\nsettles it.⟦\n\n⟧ANSWER: 55\n

**tier_a_05#54** `14_purpose_so_that.txt` [103:105] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …equation so that the leading coefficient becomes 1. Dividing by 4\ngives x*x + 2*x - 3 = 0.⟦\n\n⟧Factor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the roots are -3 and 1. We…

**tier_a_05#55** `14_purpose_so_that.txt` [164:166] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …by 4\ngives x*x + 2*x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.⟦\n\n⟧So the roots are -3 and 1. We arranged the factorization so that the signs are\nimmediate t…

**tier_a_05#56** `14_purpose_so_that.txt` [267:269] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …s are -3 and 1. We arranged the factorization so that the signs are\nimmediate to read off.⟦\n\n⟧The positive root is 1.\n\nANSWER: 1\n

**tier_a_05#57** `14_purpose_so_that.txt` [292:294] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ed the factorization so that the signs are\nimmediate to read off.\n\nThe positive root is 1.⟦\n\n⟧ANSWER: 1\n

**tier_a_05#58** `15_conditional_then.txt` [92:94] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … x is even, then x*x is divisible by 4. If x is odd, then x*x leaves\nremainder 1 modulo 8.⟦\n\n⟧Our x is 6, which is even. Then, by the first rule, 36 is divisible by 4.\nCheck: 36 = 4 * …

**tier_a_05#59** `15_conditional_then.txt` [186:188] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …r x is 6, which is even. Then, by the first rule, 36 is divisible by 4.\nCheck: 36 = 4 * 9.⟦\n\n⟧If we had started from x = 7 instead, then the second rule would apply, and\nindeed 49 = 48…

**tier_a_05#60** `15_conditional_then.txt` [311:313] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ead, then the second rule would apply, and\nindeed 49 = 48 + 1 leaves remainder 1 modulo 8.⟦\n\n⟧Thus, the divisibility claim holds for x = 6.\n\nANSWER: yes\n

**tier_a_05#61** `15_conditional_then.txt` [358:360] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ed 49 = 48 + 1 leaves remainder 1 modulo 8.\n\nThus, the divisibility claim holds for x = 6.⟦\n\n⟧ANSWER: yes\n

**tier_a_05#62** `16_enumeration.txt` [61:63] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> First, list the divisors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36.⟦\n\n⟧Second, keep only the perfect squares among them: 1, 4, 9, 36.\n\nThird, count them. There a…

**tier_a_05#63** `16_enumeration.txt` [125:127] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …2, 3, 4, 6, 9, 12, 18, 36.\n\nSecond, keep only the perfect squares among them: 1, 4, 9, 36.⟦\n\n⟧Third, count them. There are 4.\n\nNext, we double-check by the exponent formula. Since 36 =…

**tier_a_05#64** `16_enumeration.txt` [158:160] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …d, keep only the perfect squares among them: 1, 4, 9, 36.\n\nThird, count them. There are 4.⟦\n\n⟧Next, we double-check by the exponent formula. Since 36 = 2*2 * 3*3, a divisor\nis a square…

**tier_a_05#65** `16_enumeration.txt` [305:307] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … = 2*2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.⟦\n\n⟧Therefore both methods agree.\n\nANSWER: 4\n

**tier_a_05#66** `16_enumeration.txt` [336:338] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …uare iff both exponents are even, giving 2 * 2 = 4 choices.\n\nTherefore both methods agree.⟦\n\n⟧ANSWER: 4\n

**tier_a_05#67** `17_possessive_its.txt` [173:175] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …nge connectivity, because an edge exists after relabeling iff its\npreimage existed before.⟦\n\n⟧It's therefore enough to count components once. The graph has 3 components,\nand each keeps…

**tier_a_05#68** `17_possessive_its.txt` [292:294] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …unt components once. The graph has 3 components,\nand each keeps its size under relabeling.⟦\n\n⟧So the component count is 3.\n\nANSWER: 3\n

**tier_a_05#69** `17_possessive_its.txt` [322:324] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … has 3 components,\nand each keeps its size under relabeling.\n\nSo the component count is 3.⟦\n\n⟧ANSWER: 3\n

**tier_a_05#70** `18_quoted_dialogue.txt` [141:143] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …uts are positive," and the\nsecond card reads "Therefore you may take square roots freely."⟦\n\n⟧Note that the instructions quoted above are part of the puzzle text, not our\nreasoning. Ou…

**tier_a_05#71** `18_quoted_dialogue.txt` [261:263] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …uoted above are part of the puzzle text, not our\nreasoning. Our own reasoning starts here.⟦\n\n⟧We need the square root of 144, which is 12, since 12 * 12 = 144.\n\nThus, the requested val…

**tier_a_05#72** `18_quoted_dialogue.txt` [328:330] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … reasoning starts here.\n\nWe need the square root of 144, which is 12, since 12 * 12 = 144.⟦\n\n⟧Thus, the requested value is 12.\n\nANSWER: 12\n

**tier_a_05#73** `18_quoted_dialogue.txt` [362:364] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …he square root of 144, which is 12, since 12 * 12 = 144.\n\nThus, the requested value is 12.⟦\n\n⟧ANSWER: 12\n

**tier_a_05#74** `19_list_bullets.txt` [419:421] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …h congruences\n3. combine\n\nCombining x = 4 (mod 9) and x = 2 (mod 5) gives x = 22 (mod 45).⟦\n\n⟧ANSWER: 22\n

**tier_a_05#75** `20_display_lines.txt` [29:31] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> Track the value line by line.⟦\n\n⟧x = 23\nf1(x) = (11*23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, …

**tier_a_05#76** `20_display_lines.txt` [160:162] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.⟦\n\n⟧y = 63 - 40\ny = 23.\n\nSo the chain returns to its starting value after one full cycle.\n\nANS…

**tier_a_05#77** `20_display_lines.txt` [247:249] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …em.\n\ny = 63 - 40\ny = 23.\n\nSo the chain returns to its starting value after one full cycle.⟦\n\n⟧ANSWER: 23\n

**tier_a_05#78** `21_markdown_mixed.txt` [278:280] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …# Verification\n\nEach step multiplies by 3. Check: 14 * 3 = 42. So the table is consistent.⟦\n\n⟧ANSWER: 42\n

**tier_a_05#79** `22_hedging.txt` [161:163] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …\nassume. The differences are 7, 7, 7, so it is indeed arithmetic with common\ndifference 7.⟦\n\n⟧Perhaps a closed form helps: a(n) = 4 + 7*n. It seems clear that a(10) = 74.\n\nTo be safe, …

**tier_a_05#80** `22_hedging.txt` [239:241] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ifference 7.\n\nPerhaps a closed form helps: a(n) = 4 + 7*n. It seems clear that a(10) = 74.⟦\n\n⟧To be safe, check directly: 4 + 70 = 74. The hedged guess and the direct\ncomputation agree…

**tier_a_05#81** `22_hedging.txt` [354:356] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …tly: 4 + 70 = 74. The hedged guess and the direct\ncomputation agree, so the answer stands.⟦\n\n⟧ANSWER: 74\n

**tier_a_05#82** `23_lets_hortative.txt` [57:59] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> Let's compute the residue of 2 to the power 10 modulo 11.⟦\n\n⟧Fermat's little theorem lets us reduce the exponent: 2 to the power 10 is\ncongruent to 1 m…

**tier_a_05#83** `23_lets_hortative.txt` [208:210] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …he power 10 is\ncongruent to 1 modulo 11, because 11 is prime and 2 is not divisible by 11.⟦\n\n⟧Let us double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and…

**tier_a_05#84** `23_lets_hortative.txt` [390:392] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … 100 mod 11 = 1. Squaring the fifth power gives the tenth\npower, so the check confirms it.⟦\n\n⟧ANSWER: 1\n

**tier_a_05#85** `24_kitchen_sink.txt` [120:122] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …ate h(h(4)) where h(x) = x*x - 3, then report\nwhether the result lies in the range 10-200.⟦\n\n⟧It's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n…

**tier_a_05#86** `24_kitchen_sink.txt` [171:173] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …er the result lies in the range 10-200.\n\nIt's a two-step composition, so we go inside out.⟦\n\n⟧Inner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNo…

**tier_a_05#87** `24_kitchen_sink.txt` [184:186] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> … lies in the range 10-200.\n\nIt's a two-step composition, so we go inside out.\n\nInner step:⟦\n\n⟧h(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 i…

**tier_a_05#88** `24_kitchen_sink.txt` [259:261] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …t.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.⟦\n\n⟧Note that 166 is positive, and the problem said "report whether the result\nlies in the ran…

**tier_a_05#89** `24_kitchen_sink.txt` [798:800] set `inter_paragraph_gap`
  candidates: `\n\n | \n`
> …o simple it can't hide a bug\nassert h(h(4)) == 166\n```\n\nTherefore the final answer is yes.⟦\n\n⟧ANSWER: yes\n

## tier_a_06_operator_spacing — 131 sites

**tier_a_06#1** `01_multiplication_basic.txt` [20:23] set `times`
  candidates: ` *  | *`
> I need to compute 47⟦ * ⟧86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 376…

**tier_a_06#2** `01_multiplication_basic.txt` [51:54] set `plus`
  candidates: ` +  | +`
> I need to compute 47 * 86.\n\nFirst, break 86 into 80⟦ + ⟧6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow …

**tier_a_06#3** `01_multiplication_basic.txt` [68:71] set `times`
  candidates: ` *  | *`
> I need to compute 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47⟦ * ⟧80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial p…

**tier_a_06#4** `01_multiplication_basic.txt` [85:88] set `times`
  candidates: ` *  | *`
> I need to compute 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47⟦ * ⟧8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum …

**tier_a_06#5** `01_multiplication_basic.txt` [89:92] set `equals`
  candidates: ` =  | =`
> I need to compute 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8⟦ = ⟧376, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3…

**tier_a_06#6** `01_multiplication_basic.txt` [102:105] set `times`
  candidates: ` *  | *`
> …mpute 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47⟦ * ⟧80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4…

**tier_a_06#7** `01_multiplication_basic.txt` [107:110] set `equals`
  candidates: ` =  | =`
> … 47 * 86.\n\nFirst, break 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80⟦ = ⟧3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n…

**tier_a_06#8** `01_multiplication_basic.txt` [127:130] set `times`
  candidates: ` *  | *`
> …eak 86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47⟦ * ⟧6 = 282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, the product i…

**tier_a_06#9** `01_multiplication_basic.txt` [131:134] set `equals`
  candidates: ` =  | =`
> …86 into 80 + 6.\n\nCompute 47 * 80. We have 47 * 8 = 376, so 47 * 80 = 3760.\n\nCompute 47 * 6⟦ = ⟧282.\n\nNow add the partial products. The sum is 3760 + 282 = 4042.\n\nThus, the product is 40…

**tier_a_06#10** `01_multiplication_basic.txt` [185:188] set `plus`
  candidates: ` +  | +`
> …, so 47 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760⟦ + ⟧282 = 4042.\n\nThus, the product is 4042.\n\nANSWER: 4042\n

**tier_a_06#11** `01_multiplication_basic.txt` [191:194] set `equals`
  candidates: ` =  | =`
> …7 * 80 = 3760.\n\nCompute 47 * 6 = 282.\n\nNow add the partial products. The sum is 3760 + 282⟦ = ⟧4042.\n\nThus, the product is 4042.\n\nANSWER: 4042\n

**tier_a_06#12** `02_multiplication_ordinals.txt` [11:14] set `times`
  candidates: ` *  | *`
> We want 234⟦ * ⟧512. I will proceed in three stages.\n\nFirst, multiply 234 by 500. Since 234 * 5 = 1170, we…

**tier_a_06#13** `02_multiplication_ordinals.txt` [89:92] set `times`
  candidates: ` *  | *`
> We want 234 * 512. I will proceed in three stages.\n\nFirst, multiply 234 by 500. Since 234⟦ * ⟧5 = 1170, we get 234 * 500 = 117000.\n\nSecond, multiply 234 by 12. We have 234 * 12 = 2808.…

**tier_a_06#14** `02_multiplication_ordinals.txt` [93:96] set `equals`
  candidates: ` =  | =`
> …want 234 * 512. I will proceed in three stages.\n\nFirst, multiply 234 by 500. Since 234 * 5⟦ = ⟧1170, we get 234 * 500 = 117000.\n\nSecond, multiply 234 by 12. We have 234 * 12 = 2808.\n\nTh…

**tier_a_06#15** `02_multiplication_ordinals.txt` [112:115] set `times`
  candidates: ` *  | *`
> …ill proceed in three stages.\n\nFirst, multiply 234 by 500. Since 234 * 5 = 1170, we get 234⟦ * ⟧500 = 117000.\n\nSecond, multiply 234 by 12. We have 234 * 12 = 2808.\n\nThird, add the two pa…

**tier_a_06#16** `02_multiplication_ordinals.txt` [118:121] set `equals`
  candidates: ` =  | =`
> …oceed in three stages.\n\nFirst, multiply 234 by 500. Since 234 * 5 = 1170, we get 234 * 500⟦ = ⟧117000.\n\nSecond, multiply 234 by 12. We have 234 * 12 = 2808.\n\nThird, add the two partial …

**tier_a_06#17** `02_multiplication_ordinals.txt` [169:172] set `times`
  candidates: ` *  | *`
> … Since 234 * 5 = 1170, we get 234 * 500 = 117000.\n\nSecond, multiply 234 by 12. We have 234⟦ * ⟧12 = 2808.\n\nThird, add the two partial results. The total is 117000 + 2808 = 119808.\n\nTher…

**tier_a_06#18** `02_multiplication_ordinals.txt` [174:177] set `equals`
  candidates: ` =  | =`
> …e 234 * 5 = 1170, we get 234 * 500 = 117000.\n\nSecond, multiply 234 by 12. We have 234 * 12⟦ = ⟧2808.\n\nThird, add the two partial results. The total is 117000 + 2808 = 119808.\n\nTherefore…

**tier_a_06#19** `02_multiplication_ordinals.txt` [239:242] set `plus`
  candidates: ` +  | +`
> …4 by 12. We have 234 * 12 = 2808.\n\nThird, add the two partial results. The total is 117000⟦ + ⟧2808 = 119808.\n\nTherefore the answer is 119808.\n\nANSWER: 119808\n

**tier_a_06#20** `02_multiplication_ordinals.txt` [246:249] set `equals`
  candidates: ` =  | =`
> …. We have 234 * 12 = 2808.\n\nThird, add the two partial results. The total is 117000 + 2808⟦ = ⟧119808.\n\nTherefore the answer is 119808.\n\nANSWER: 119808\n

**tier_a_06#21** `03_composition_chain.txt` [58:61] set `equals`
  candidates: ` =  | =`
> We evaluate the chain from the inside out, starting with x⟦ = ⟧23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow re…

**tier_a_06#22** `03_composition_chain.txt` [88:89] set `times`
  candidates: `* |  * `
> We evaluate the chain from the inside out, starting with x = 23.\n\nApply f1. f1(23) = (11⟦*⟧23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen…

**tier_a_06#23** `03_composition_chain.txt` [91:94] set `plus`
  candidates: ` +  | +`
> …e evaluate the chain from the inside out, starting with x = 23.\n\nApply f1. f1(23) = (11*23⟦ + ⟧4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, app…

**tier_a_06#24** `03_composition_chain.txt` [115:116] set `times`
  candidates: `* |  * `
> …m the inside out, starting with x = 23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11⟦*⟧23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = …

**tier_a_06#25** `03_composition_chain.txt` [118:121] set `equals`
  candidates: ` =  | =`
> …he inside out, starting with x = 23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23⟦ = ⟧253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63…

**tier_a_06#26** `03_composition_chain.txt` [133:136] set `plus`
  candidates: ` +  | +`
> …starting with x = 23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253⟦ + ⟧4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nC…

**tier_a_06#27** `03_composition_chain.txt` [137:140] set `equals`
  candidates: ` =  | =`
> …ting with x = 23.\n\nApply f1. f1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4⟦ = ⟧257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompu…

**tier_a_06#28** `03_composition_chain.txt` [167:170] set `equals`
  candidates: ` =  | =`
> …1(23) = (11*23 + 4) mod 97. Compute 11*23 = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97⟦ = ⟧63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = …

**tier_a_06#29** `03_composition_chain.txt` [208:209] set `times`
  candidates: `* |  * `
> … = 253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7⟦*⟧63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, …

**tier_a_06#30** `03_composition_chain.txt` [211:214] set `plus`
  candidates: ` +  | +`
> …253, and 253 + 4 = 257.\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63⟦ + ⟧90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply…

**tier_a_06#31** `03_composition_chain.txt` [234:235] set `times`
  candidates: `* |  * `
> …\nNow reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7⟦*⟧63 = 441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(…

**tier_a_06#32** `03_composition_chain.txt` [237:240] set `equals`
  candidates: ` =  | =`
> …w reduce: 257 mod 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63⟦ = ⟧441, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) =…

**tier_a_06#33** `03_composition_chain.txt` [252:255] set `plus`
  candidates: ` +  | +`
> …od 97 = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441⟦ + ⟧90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod…

**tier_a_06#34** `03_composition_chain.txt` [257:260] set `equals`
  candidates: ` =  | =`
> … = 63.\n\nThen, apply f2 to 63.\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90⟦ = ⟧531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 =…

**tier_a_06#35** `03_composition_chain.txt` [285:288] set `equals`
  candidates: ` =  | =`
> ….\nf2(63) = (7*63 + 90) mod 97\nCompute 7*63 = 441, and 441 + 90 = 531. We reduce 531 mod 97⟦ = ⟧46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97 = 93.\n\nSo the final value is …

**tier_a_06#36** `03_composition_chain.txt` [333:334] set `times`
  candidates: `* |  * `
> …, and 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2⟦*⟧46 + 1) mod 97 = 93.\n\nSo the final value is 93.\n\nANSWER: 93\n

**tier_a_06#37** `03_composition_chain.txt` [336:339] set `plus`
  candidates: ` +  | +`
> …nd 441 + 90 = 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46⟦ + ⟧1) mod 97 = 93.\n\nSo the final value is 93.\n\nANSWER: 93\n

**tier_a_06#38** `03_composition_chain.txt` [348:351] set `equals`
  candidates: ` =  | =`
> …= 531. We reduce 531 mod 97 = 46.\n\nNext, apply f3 to 46. We get f3(46) = (2*46 + 1) mod 97⟦ = ⟧93.\n\nSo the final value is 93.\n\nANSWER: 93\n

**tier_a_06#39** `04_composition_negative.txt` [15:18] set `equals`
  candidates: ` =  | =`
> The map is g(x)⟦ = ⟧3*x - 5, applied twice to x = -4.\n\nFirst application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.\n…

**tier_a_06#40** `04_composition_negative.txt` [19:20] set `times`
  candidates: `* |  * `
> The map is g(x) = 3⟦*⟧x - 5, applied twice to x = -4.\n\nFirst application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.\n\nS…

**tier_a_06#41** `04_composition_negative.txt` [21:24] set `binary_minus`
  candidates: ` -  | -`
> The map is g(x) = 3*x⟦ - ⟧5, applied twice to x = -4.\n\nFirst application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.\n\nSecon…

**tier_a_06#42** `04_composition_negative.txt` [77:80] set `equals`
  candidates: ` =  | =`
> The map is g(x) = 3*x - 5, applied twice to x = -4.\n\nFirst application: g(-4)⟦ = ⟧3*(-4) - 5 = -12 - 5 = -17.\n\nSecond application: g(-17) = 3*(-17) - 5 = -51 - 5 = -56.\n\nNo…

**tier_a_06#43** `04_composition_negative.txt` [135:138] set `equals`
  candidates: ` =  | =`
> … = -4.\n\nFirst application: g(-4) = 3*(-4) - 5 = -12 - 5 = -17.\n\nSecond application: g(-17)⟦ = ⟧3*(-17) - 5 = -51 - 5 = -56.\n\nNote that the sign stays negative throughout, since each ste…

**tier_a_06#44** `07_prose_geometry.txt` [80:81] set `times`
  candidates: `* |  * `
> Consider the triangle with sides 5, 12, and 13. It's a right triangle, because\n5⟦*⟧5 + 12*12 = 25 + 144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe trian…

**tier_a_06#45** `07_prose_geometry.txt` [82:85] set `plus`
  candidates: ` +  | +`
> Consider the triangle with sides 5, 12, and 13. It's a right triangle, because\n5*5⟦ + ⟧12*12 = 25 + 144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle …

**tier_a_06#46** `07_prose_geometry.txt` [87:88] set `times`
  candidates: `* |  * `
> Consider the triangle with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12⟦*⟧12 = 25 + 144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle kee…

**tier_a_06#47** `07_prose_geometry.txt` [90:93] set `equals`
  candidates: ` =  | =`
> Consider the triangle with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12*12⟦ = ⟧25 + 144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle keeps it…

**tier_a_06#48** `07_prose_geometry.txt` [95:98] set `plus`
  candidates: ` +  | +`
> …der the triangle with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12*12 = 25⟦ + ⟧144 = 169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle keeps its rig…

**tier_a_06#49** `07_prose_geometry.txt` [101:104] set `equals`
  candidates: ` =  | =`
> …e triangle with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12*12 = 25 + 144⟦ = ⟧169 = 13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle keeps its right ang…

**tier_a_06#50** `07_prose_geometry.txt` [107:110] set `equals`
  candidates: ` =  | =`
> …ngle with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12*12 = 25 + 144 = 169⟦ = ⟧13*13, which is exactly the Pythagorean\ncondition.\n\nThe triangle keeps its right angle und…

**tier_a_06#51** `07_prose_geometry.txt` [112:113] set `times`
  candidates: `* |  * `
> …with sides 5, 12, and 13. It's a right triangle, because\n5*5 + 12*12 = 25 + 144 = 169 = 13⟦*⟧13, which is exactly the Pythagorean\ncondition.\n\nThe triangle keeps its right angle under …

**tier_a_06#52** `07_prose_geometry.txt` [439:442] set `times`
  candidates: ` *  | *`
> …s changing orientation, but orientation\ndoes not affect side lengths. Thus, the area is (5⟦ * ⟧12) / 2 = 30.\n\nANSWER: 30\n

**tier_a_06#53** `07_prose_geometry.txt` [449:452] set `equals`
  candidates: ` =  | =`
> … orientation, but orientation\ndoes not affect side lengths. Thus, the area is (5 * 12) / 2⟦ = ⟧30.\n\nANSWER: 30\n

**tier_a_06#54** `08_prose_quotes.txt` [163:166] set `equals`
  candidates: ` =  | =`
> … it\ndivides one of the factors." This is Euclid's lemma.\n\nNote that 7 divides 84, since 84⟦ = ⟧7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that 21 * 4 = 84. So the answe…

**tier_a_06#55** `08_prose_quotes.txt` [167:170] set `times`
  candidates: ` *  | *`
> …divides one of the factors." This is Euclid's lemma.\n\nNote that 7 divides 84, since 84 = 7⟦ * ⟧12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that 21 * 4 = 84. So the answer fo…

**tier_a_06#56** `08_prose_quotes.txt` [211:214] set `times`
  candidates: ` *  | *`
> …s lemma.\n\nNote that 7 divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21⟦ * ⟧4.\n\nObserve that 21 * 4 = 84. So the answer follows directly: 7 divides 21 * 4, and\nby the…

**tier_a_06#57** `08_prose_quotes.txt` [233:236] set `times`
  candidates: ` *  | *`
> …divides 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that 21⟦ * ⟧4 = 84. So the answer follows directly: 7 divides 21 * 4, and\nby the quoted lemma 7 must d…

**tier_a_06#58** `08_prose_quotes.txt` [237:240] set `equals`
  candidates: ` =  | =`
> …des 84, since 84 = 7 * 12. The problem asks whether 7 divides\n21 * 4.\n\nObserve that 21 * 4⟦ = ⟧84. So the answer follows directly: 7 divides 21 * 4, and\nby the quoted lemma 7 must divid…

**tier_a_06#59** `08_prose_quotes.txt` [288:291] set `times`
  candidates: ` *  | *`
> … 7 divides\n21 * 4.\n\nObserve that 21 * 4 = 84. So the answer follows directly: 7 divides 21⟦ * ⟧4, and\nby the quoted lemma 7 must divide 21 or divide 4. Indeed 21 = 7 * 3.\n\nThe hint said…

**tier_a_06#60** `08_prose_quotes.txt` [357:360] set `equals`
  candidates: ` =  | =`
> …irectly: 7 divides 21 * 4, and\nby the quoted lemma 7 must divide 21 or divide 4. Indeed 21⟦ = ⟧7 * 3.\n\nThe hint said "Thus, use the lemma directly," and that is what we did.\n\nANSWER: ye…

**tier_a_06#61** `08_prose_quotes.txt` [361:364] set `times`
  candidates: ` *  | *`
> …tly: 7 divides 21 * 4, and\nby the quoted lemma 7 must divide 21 or divide 4. Indeed 21 = 7⟦ * ⟧3.\n\nThe hint said "Thus, use the lemma directly," and that is what we did.\n\nANSWER: yes\n

**tier_a_06#62** `11_ranges.txt` [193:196] set `times`
  candidates: ` *  | *`
> … is 7 (integer midpoint, rounding down from\n7.5). Pick offset 2.\n\nNow compute the index: 7⟦ * ⟧3 - 2 = 21 - 2 = 19.\n\nSo the index is 19, which lies outside 5-10, as required.\n\nANSWER: 1…

**tier_a_06#63** `11_ranges.txt` [201:204] set `equals`
  candidates: ` =  | =`
> …nteger midpoint, rounding down from\n7.5). Pick offset 2.\n\nNow compute the index: 7 * 3 - 2⟦ = ⟧21 - 2 = 19.\n\nSo the index is 19, which lies outside 5-10, as required.\n\nANSWER: 19\n

**tier_a_06#64** `11_ranges.txt` [210:213] set `equals`
  candidates: ` =  | =`
> …dpoint, rounding down from\n7.5). Pick offset 2.\n\nNow compute the index: 7 * 3 - 2 = 21 - 2⟦ = ⟧19.\n\nSo the index is 19, which lies outside 5-10, as required.\n\nANSWER: 19\n

**tier_a_06#65** `13_comparative_so.txt` [169:172] set `equals`
  candidates: ` =  | =`
> …t entirely for large n.\n\nThe bound we derived is so loose that it tells us nothing below n⟦ = ⟧100. For\nsmall n we compute directly.\n\nAt n = 10 the sum is 55, so the direct value is wha…

**tier_a_06#66** `13_comparative_so.txt` [215:218] set `equals`
  candidates: ` =  | =`
> …is so loose that it tells us nothing below n = 100. For\nsmall n we compute directly.\n\nAt n⟦ = ⟧10 the sum is 55, so the direct value is what we report. The gap\nbetween the bound and the…

**tier_a_06#67** `14_purpose_so_that.txt` [86:87] set `times`
  candidates: `* |  * `
> We scale the equation so that the leading coefficient becomes 1. Dividing by 4\ngives x⟦*⟧x + 2*x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the root…

**tier_a_06#68** `14_purpose_so_that.txt` [88:91] set `plus`
  candidates: ` +  | +`
> We scale the equation so that the leading coefficient becomes 1. Dividing by 4\ngives x*x⟦ + ⟧2*x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the roots ar…

**tier_a_06#69** `14_purpose_so_that.txt` [92:93] set `times`
  candidates: `* |  * `
> … scale the equation so that the leading coefficient becomes 1. Dividing by 4\ngives x*x + 2⟦*⟧x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the roots are …

**tier_a_06#70** `14_purpose_so_that.txt` [94:97] set `binary_minus`
  candidates: ` -  | -`
> …cale the equation so that the leading coefficient becomes 1. Dividing by 4\ngives x*x + 2*x⟦ - ⟧3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the roots are -3 a…

**tier_a_06#71** `14_purpose_so_that.txt` [98:101] set `equals`
  candidates: ` =  | =`
> … the equation so that the leading coefficient becomes 1. Dividing by 4\ngives x*x + 2*x - 3⟦ = ⟧0.\n\nFactor it so that each root is visible: (x + 3)(x - 1) = 0.\n\nSo the roots are -3 and 1…

**tier_a_06#72** `14_purpose_so_that.txt` [147:150] set `plus`
  candidates: ` +  | +`
> …omes 1. Dividing by 4\ngives x*x + 2*x - 3 = 0.\n\nFactor it so that each root is visible: (x⟦ + ⟧3)(x - 1) = 0.\n\nSo the roots are -3 and 1. We arranged the factorization so that the signs…

**tier_a_06#73** `14_purpose_so_that.txt` [154:157] set `binary_minus`
  candidates: ` -  | -`
> … Dividing by 4\ngives x*x + 2*x - 3 = 0.\n\nFactor it so that each root is visible: (x + 3)(x⟦ - ⟧1) = 0.\n\nSo the roots are -3 and 1. We arranged the factorization so that the signs are\nim…

**tier_a_06#74** `15_conditional_then.txt` [20:21] set `times`
  candidates: `* |  * `
> If x is even, then x⟦*⟧x is divisible by 4. If x is odd, then x*x leaves\nremainder 1 modulo 8.\n\nOur x is 6, which…

**tier_a_06#75** `15_conditional_then.txt` [61:62] set `times`
  candidates: `* |  * `
> If x is even, then x*x is divisible by 4. If x is odd, then x⟦*⟧x leaves\nremainder 1 modulo 8.\n\nOur x is 6, which is even. Then, by the first rule, 36 is …

**tier_a_06#76** `15_conditional_then.txt` [177:180] set `equals`
  candidates: ` =  | =`
> …lo 8.\n\nOur x is 6, which is even. Then, by the first rule, 36 is divisible by 4.\nCheck: 36⟦ = ⟧4 * 9.\n\nIf we had started from x = 7 instead, then the second rule would apply, and\nindeed…

**tier_a_06#77** `15_conditional_then.txt` [181:184] set `times`
  candidates: ` *  | *`
> ….\n\nOur x is 6, which is even. Then, by the first rule, 36 is divisible by 4.\nCheck: 36 = 4⟦ * ⟧9.\n\nIf we had started from x = 7 instead, then the second rule would apply, and\nindeed 49 …

**tier_a_06#78** `15_conditional_then.txt` [212:215] set `equals`
  candidates: ` =  | =`
> …hen, by the first rule, 36 is divisible by 4.\nCheck: 36 = 4 * 9.\n\nIf we had started from x⟦ = ⟧7 instead, then the second rule would apply, and\nindeed 49 = 48 + 1 leaves remainder 1 mod…

**tier_a_06#79** `15_conditional_then.txt` [273:276] set `equals`
  candidates: ` =  | =`
> … 9.\n\nIf we had started from x = 7 instead, then the second rule would apply, and\nindeed 49⟦ = ⟧48 + 1 leaves remainder 1 modulo 8.\n\nThus, the divisibility claim holds for x = 6.\n\nANSWER…

**tier_a_06#80** `15_conditional_then.txt` [278:281] set `plus`
  candidates: ` +  | +`
> …If we had started from x = 7 instead, then the second rule would apply, and\nindeed 49 = 48⟦ + ⟧1 leaves remainder 1 modulo 8.\n\nThus, the divisibility claim holds for x = 6.\n\nANSWER: yes…

**tier_a_06#81** `15_conditional_then.txt` [353:356] set `equals`
  candidates: ` =  | =`
> …\nindeed 49 = 48 + 1 leaves remainder 1 modulo 8.\n\nThus, the divisibility claim holds for x⟦ = ⟧6.\n\nANSWER: yes\n

**tier_a_06#82** `16_enumeration.txt` [215:218] set `equals`
  candidates: ` =  | =`
> …\n\nThird, count them. There are 4.\n\nNext, we double-check by the exponent formula. Since 36⟦ = ⟧2*2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.\n\nT…

**tier_a_06#83** `16_enumeration.txt` [219:220] set `times`
  candidates: `* |  * `
> …ird, count them. There are 4.\n\nNext, we double-check by the exponent formula. Since 36 = 2⟦*⟧2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.\n\nThe…

**tier_a_06#84** `16_enumeration.txt` [221:224] set `times`
  candidates: ` *  | *`
> …d, count them. There are 4.\n\nNext, we double-check by the exponent formula. Since 36 = 2*2⟦ * ⟧3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.\n\nTherefo…

**tier_a_06#85** `16_enumeration.txt` [225:226] set `times`
  candidates: `* |  * `
> …ount them. There are 4.\n\nNext, we double-check by the exponent formula. Since 36 = 2*2 * 3⟦*⟧3, a divisor\nis a square iff both exponents are even, giving 2 * 2 = 4 choices.\n\nTherefore…

**tier_a_06#86** `16_enumeration.txt` [288:291] set `times`
  candidates: ` *  | *`
> …formula. Since 36 = 2*2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2⟦ * ⟧2 = 4 choices.\n\nTherefore both methods agree.\n\nANSWER: 4\n

**tier_a_06#87** `16_enumeration.txt` [292:295] set `equals`
  candidates: ` =  | =`
> …ula. Since 36 = 2*2 * 3*3, a divisor\nis a square iff both exponents are even, giving 2 * 2⟦ = ⟧4 choices.\n\nTherefore both methods agree.\n\nANSWER: 4\n

**tier_a_06#88** `18_quoted_dialogue.txt` [316:319] set `times`
  candidates: ` *  | *`
> …ing. Our own reasoning starts here.\n\nWe need the square root of 144, which is 12, since 12⟦ * ⟧12 = 144.\n\nThus, the requested value is 12.\n\nANSWER: 12\n

**tier_a_06#89** `18_quoted_dialogue.txt` [321:324] set `equals`
  candidates: ` =  | =`
> …Our own reasoning starts here.\n\nWe need the square root of 144, which is 12, since 12 * 12⟦ = ⟧144.\n\nThus, the requested value is 12.\n\nANSWER: 12\n

**tier_a_06#90** `19_list_bullets.txt` [199:202] set `times`
  candidates: ` *  | *`
> …\n- combine the solutions with the CRT\n\nApplied to our case:\n\n* the modulus 45 factors as 9⟦ * ⟧5\n* modulo 9 the solution is x = 4\n* modulo 5 the solution is x = 2\n\nNumbered recap for th…

**tier_a_06#91** `19_list_bullets.txt` [232:235] set `equals`
  candidates: ` =  | =`
> … CRT\n\nApplied to our case:\n\n* the modulus 45 factors as 9 * 5\n* modulo 9 the solution is x⟦ = ⟧4\n* modulo 5 the solution is x = 2\n\nNumbered recap for the writeup:\n\n1. factor 45\n2. solve…

**tier_a_06#92** `19_list_bullets.txt` [265:268] set `equals`
  candidates: ` =  | =`
> … modulus 45 factors as 9 * 5\n* modulo 9 the solution is x = 4\n* modulo 5 the solution is x⟦ = ⟧2\n\nNumbered recap for the writeup:\n\n1. factor 45\n2. solve both congruences\n3. combine\n\nCom…

**tier_a_06#93** `19_list_bullets.txt` [366:369] set `equals`
  candidates: ` =  | =`
> …red recap for the writeup:\n\n1. factor 45\n2. solve both congruences\n3. combine\n\nCombining x⟦ = ⟧4 (mod 9) and x = 2 (mod 5) gives x = 22 (mod 45).\n\nANSWER: 22\n

**tier_a_06#94** `19_list_bullets.txt` [384:387] set `equals`
  candidates: ` =  | =`
> …writeup:\n\n1. factor 45\n2. solve both congruences\n3. combine\n\nCombining x = 4 (mod 9) and x⟦ = ⟧2 (mod 5) gives x = 22 (mod 45).\n\nANSWER: 22\n

**tier_a_06#95** `19_list_bullets.txt` [404:407] set `equals`
  candidates: ` =  | =`
> …45\n2. solve both congruences\n3. combine\n\nCombining x = 4 (mod 9) and x = 2 (mod 5) gives x⟦ = ⟧22 (mod 45).\n\nANSWER: 22\n

**tier_a_06#96** `20_display_lines.txt` [32:35] set `equals`
  candidates: ` =  | =`
> Track the value line by line.\n\nx⟦ = ⟧23\nf1(x) = (11*23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but …

**tier_a_06#97** `20_display_lines.txt` [49:50] set `times`
  candidates: `* |  * `
> Track the value line by line.\n\nx = 23\nf1(x) = (11⟦*⟧23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stay…

**tier_a_06#98** `20_display_lines.txt` [52:55] set `plus`
  candidates: ` +  | +`
> Track the value line by line.\n\nx = 23\nf1(x) = (11*23⟦ + ⟧4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 i…

**tier_a_06#99** `20_display_lines.txt` [70:73] set `equals`
  candidates: ` =  | =`
> Track the value line by line.\n\nx = 23\nf1(x) = (11*23 + 4) mod 97\nf1(x)⟦ = ⟧63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny…

**tier_a_06#100** `20_display_lines.txt` [111:114] set `times`
  candidates: ` *  | *`
> …by line.\n\nx = 23\nf1(x) = (11*23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5⟦ * ⟧4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40\ny = 23.\n\nSo the chain returns …

**tier_a_06#101** `20_display_lines.txt` [115:118] set `equals`
  candidates: ` =  | =`
> …ine.\n\nx = 23\nf1(x) = (11*23 + 4) mod 97\nf1(x) = 63.\n\nHalving the offset would give 0.5 * 4⟦ = ⟧2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40\ny = 23.\n\nSo the chain returns to i…

**tier_a_06#102** `20_display_lines.txt` [163:166] set `equals`
  candidates: ` =  | =`
> …63.\n\nHalving the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny⟦ = ⟧63 - 40\ny = 23.\n\nSo the chain returns to its starting value after one full cycle.\n\nANSWER:…

**tier_a_06#103** `20_display_lines.txt` [175:178] set `equals`
  candidates: ` =  | =`
> … the offset would give 0.5 * 4 = 2, but the offset stays 4 in this\nproblem.\n\ny = 63 - 40\ny⟦ = ⟧23.\n\nSo the chain returns to its starting value after one full cycle.\n\nANSWER: 23\n

**tier_a_06#104** `21_markdown_mixed.txt` [240:243] set `times`
  candidates: ` *  | *`
> … row, the value after step 2 is 42.\n\n## Verification\n\nEach step multiplies by 3. Check: 14⟦ * ⟧3 = 42. So the table is consistent.\n\nANSWER: 42\n

**tier_a_06#105** `21_markdown_mixed.txt` [244:247] set `equals`
  candidates: ` =  | =`
> …, the value after step 2 is 42.\n\n## Verification\n\nEach step multiplies by 3. Check: 14 * 3⟦ = ⟧42. So the table is consistent.\n\nANSWER: 42\n

**tier_a_06#106** `22_hedging.txt` [196:199] set `equals`
  candidates: ` =  | =`
> …7, so it is indeed arithmetic with common\ndifference 7.\n\nPerhaps a closed form helps: a(n)⟦ = ⟧4 + 7*n. It seems clear that a(10) = 74.\n\nTo be safe, check directly: 4 + 70 = 74. The hed…

**tier_a_06#107** `22_hedging.txt` [200:203] set `plus`
  candidates: ` +  | +`
> …o it is indeed arithmetic with common\ndifference 7.\n\nPerhaps a closed form helps: a(n) = 4⟦ + ⟧7*n. It seems clear that a(10) = 74.\n\nTo be safe, check directly: 4 + 70 = 74. The hedged …

**tier_a_06#108** `22_hedging.txt` [204:205] set `times`
  candidates: `* |  * `
> … is indeed arithmetic with common\ndifference 7.\n\nPerhaps a closed form helps: a(n) = 4 + 7⟦*⟧n. It seems clear that a(10) = 74.\n\nTo be safe, check directly: 4 + 70 = 74. The hedged gu…

**tier_a_06#109** `22_hedging.txt` [233:236] set `equals`
  candidates: ` =  | =`
> …mmon\ndifference 7.\n\nPerhaps a closed form helps: a(n) = 4 + 7*n. It seems clear that a(10)⟦ = ⟧74.\n\nTo be safe, check directly: 4 + 70 = 74. The hedged guess and the direct\ncomputation …

**tier_a_06#110** `22_hedging.txt` [270:273] set `plus`
  candidates: ` +  | +`
> …form helps: a(n) = 4 + 7*n. It seems clear that a(10) = 74.\n\nTo be safe, check directly: 4⟦ + ⟧70 = 74. The hedged guess and the direct\ncomputation agree, so the answer stands.\n\nANSWER:…

**tier_a_06#111** `22_hedging.txt` [275:278] set `equals`
  candidates: ` =  | =`
> …helps: a(n) = 4 + 7*n. It seems clear that a(10) = 74.\n\nTo be safe, check directly: 4 + 70⟦ = ⟧74. The hedged guess and the direct\ncomputation agree, so the answer stands.\n\nANSWER: 74\n

**tier_a_06#112** `23_lets_hortative.txt` [245:248] set `equals`
  candidates: ` =  | =`
> …11, because 11 is prime and 2 is not divisible by 11.\n\nLet us double-check by squaring: 32⟦ = ⟧2*2*2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth po…

**tier_a_06#113** `23_lets_hortative.txt` [249:250] set `times`
  candidates: `* |  * `
> …because 11 is prime and 2 is not divisible by 11.\n\nLet us double-check by squaring: 32 = 2⟦*⟧2*2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth powe…

**tier_a_06#114** `23_lets_hortative.txt` [251:252] set `times`
  candidates: `* |  * `
> …cause 11 is prime and 2 is not divisible by 11.\n\nLet us double-check by squaring: 32 = 2*2⟦*⟧2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth power …

**tier_a_06#115** `23_lets_hortative.txt` [253:254] set `times`
  candidates: `* |  * `
> …use 11 is prime and 2 is not divisible by 11.\n\nLet us double-check by squaring: 32 = 2*2*2⟦*⟧2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth power gi…

**tier_a_06#116** `23_lets_hortative.txt` [255:256] set `times`
  candidates: `* |  * `
> …e 11 is prime and 2 is not divisible by 11.\n\nLet us double-check by squaring: 32 = 2*2*2*2⟦*⟧2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth power give…

**tier_a_06#117** `23_lets_hortative.txt` [272:275] set `equals`
  candidates: ` =  | =`
> … 2 is not divisible by 11.\n\nLet us double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11⟦ = ⟧10, then\n10*10 = 100, and 100 mod 11 = 1. Squaring the fifth power gives the tenth\npower, …

**tier_a_06#118** `23_lets_hortative.txt` [286:287] set `times`
  candidates: `* |  * `
> …sible by 11.\n\nLet us double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, then\n10⟦*⟧10 = 100, and 100 mod 11 = 1. Squaring the fifth power gives the tenth\npower, so the check…

**tier_a_06#119** `23_lets_hortative.txt` [289:292] set `equals`
  candidates: ` =  | =`
> …le by 11.\n\nLet us double-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, then\n10*10⟦ = ⟧100, and 100 mod 11 = 1. Squaring the fifth power gives the tenth\npower, so the check conf…

**tier_a_06#120** `23_lets_hortative.txt` [311:314] set `equals`
  candidates: ` =  | =`
> …le-check by squaring: 32 = 2*2*2*2*2, and 32 mod 11 = 10, then\n10*10 = 100, and 100 mod 11⟦ = ⟧1. Squaring the fifth power gives the tenth\npower, so the check confirms it.\n\nANSWER: 1\n

**tier_a_06#121** `24_kitchen_sink.txt` [52:55] set `equals`
  candidates: ` =  | =`
> First, restate the task: evaluate h(h(4)) where h(x)⟦ = ⟧x*x - 3, then report\nwhether the result lies in the range 10-200.\n\nIt's a two-step composi…

**tier_a_06#122** `24_kitchen_sink.txt` [56:57] set `times`
  candidates: `* |  * `
> First, restate the task: evaluate h(h(4)) where h(x) = x⟦*⟧x - 3, then report\nwhether the result lies in the range 10-200.\n\nIt's a two-step compositi…

**tier_a_06#123** `24_kitchen_sink.txt` [58:61] set `binary_minus`
  candidates: ` -  | -`
> First, restate the task: evaluate h(h(4)) where h(x) = x*x⟦ - ⟧3, then report\nwhether the result lies in the range 10-200.\n\nIt's a two-step composition, …

**tier_a_06#124** `24_kitchen_sink.txt` [190:193] set `equals`
  candidates: ` =  | =`
> …in the range 10-200.\n\nIt's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4)⟦ = ⟧4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is posit…

**tier_a_06#125** `24_kitchen_sink.txt` [194:195] set `times`
  candidates: `* |  * `
> …he range 10-200.\n\nIt's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4⟦*⟧4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positiv…

**tier_a_06#126** `24_kitchen_sink.txt` [205:208] set `equals`
  candidates: ` =  | =`
> …-200.\n\nIt's a two-step composition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4)⟦ = ⟧13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positive, and the pr…

**tier_a_06#127** `24_kitchen_sink.txt` [230:233] set `equals`
  candidates: ` =  | =`
> …mposition, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13)⟦ = ⟧13*13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positive, and the problem said "report whethe…

**tier_a_06#128** `24_kitchen_sink.txt` [235:236] set `times`
  candidates: `* |  * `
> …tion, so we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13⟦*⟧13 - 3 = 169 - 3 = 166.\n\nNote that 166 is positive, and the problem said "report whether t…

**tier_a_06#129** `24_kitchen_sink.txt` [242:245] set `equals`
  candidates: ` =  | =`
> …o we go inside out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3⟦ = ⟧169 - 3 = 166.\n\nNote that 166 is positive, and the problem said "report whether the result…

**tier_a_06#130** `24_kitchen_sink.txt` [252:255] set `equals`
  candidates: ` =  | =`
> …side out.\n\nInner step:\n\nh(4) = 4*4 - 3\nh(4) = 13.\n\nOuter step: h(13) = 13*13 - 3 = 169 - 3⟦ = ⟧166.\n\nNote that 166 is positive, and the problem said "report whether the result\nlies in t…

**tier_a_06#131** `24_kitchen_sink.txt` [625:626] set `times`
  candidates: `* |  * `
> …and its verification needed only two comparisons. We can't\nskip the bounds check, since 13⟦*⟧13 might plausibly have exceeded 200.\n\n```python\ndef h(x):\n    return x*x - 3  # so simple…

## tier_a_07_list_markers — 8 sites

**tier_a_07#1** `19_list_bullets.txt` [33:35] set `bullet_glyph`
  candidates: `-  | * `
> The algorithm has three phases:\n\n⟦- ⟧factor the modulus into primes\n- solve the congruence for each prime power\n- combine the s…

**tier_a_07#2** `19_list_bullets.txt` [66:68] set `bullet_glyph`
  candidates: `-  | * `
> The algorithm has three phases:\n\n- factor the modulus into primes\n⟦- ⟧solve the congruence for each prime power\n- combine the solutions with the CRT\n\nApplied to…

**tier_a_07#3** `19_list_bullets.txt` [110:112] set `bullet_glyph`
  candidates: `-  | * `
> …ree phases:\n\n- factor the modulus into primes\n- solve the congruence for each prime power\n⟦- ⟧combine the solutions with the CRT\n\nApplied to our case:\n\n* the modulus 45 factors as 9 * …

**tier_a_07#4** `19_list_bullets.txt` [170:172] set `bullet_glyph`
  candidates: `*  | - `
> …ngruence for each prime power\n- combine the solutions with the CRT\n\nApplied to our case:\n\n⟦* ⟧the modulus 45 factors as 9 * 5\n* modulo 9 the solution is x = 4\n* modulo 5 the solution i…

**tier_a_07#5** `19_list_bullets.txt` [204:206] set `bullet_glyph`
  candidates: `*  | - `
> …mbine the solutions with the CRT\n\nApplied to our case:\n\n* the modulus 45 factors as 9 * 5\n⟦* ⟧modulo 9 the solution is x = 4\n* modulo 5 the solution is x = 2\n\nNumbered recap for the wr…

**tier_a_07#6** `19_list_bullets.txt` [237:239] set `bullet_glyph`
  candidates: `*  | - `
> …\nApplied to our case:\n\n* the modulus 45 factors as 9 * 5\n* modulo 9 the solution is x = 4\n⟦* ⟧modulo 5 the solution is x = 2\n\nNumbered recap for the writeup:\n\n1. factor 45\n2. solve bot…

**tier_a_07#7** `24_kitchen_sink.txt` [380:382] set `bullet_glyph`
  candidates: `-  | * `
> …d the problem said "report whether the result\nlies in the range," so that is what we do:\n\n⟦- ⟧lower bound: 166 >= 10 holds\n- upper bound: 166 <= 200 holds\n\nIf both bounds hold, then th…

**tier_a_07#8** `24_kitchen_sink.txt` [411:413] set `bullet_glyph`
  candidates: `-  | * `
> …her the result\nlies in the range," so that is what we do:\n\n- lower bound: 166 >= 10 holds\n⟦- ⟧upper bound: 166 <= 200 holds\n\nIf both bounds hold, then the value lies in the range. Both…

## Rules with zero sites in this corpus

- none — every rule produced at least one site

## Rule 01 effective-power log (REVIEW_LOG F4)

Candidate connective occurrences considered, by outcome:
- masked_quote_or_code: 11
- matched: 31
- position_invalid: 10

Rule 03 sequencing set: structurally unavailable per REVIEW_LOG F1
(density is a structural zero, not an observed zero).
