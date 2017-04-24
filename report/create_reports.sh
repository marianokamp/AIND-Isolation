#!/bin/sh
cd report
pandoc -f markdown+tex_math_single_backslash -o heuristic_analysis.pdf heuristic_analysis.md
pandoc -f markdown+tex_math_single_backslash -o research_review.pdf research_review.md 
mv *.pdf ../.
cd -
