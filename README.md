# Citation manager

Automatic convert bibtex format citation to bibitem in the .tex file. (Currently support conference CCDC and journal CVM).

Like the json file, the emergence of the bibtex citation format should be to simplify the citation process. However, the existing latex software cannot read the information contained in bibtex, and different journals have different requirements for the citation format. 

In response to this problem, I wrote this python program to assist me in writing my thesis.

## Requirements
- Python3
- Python Lib: re

## Usage
Creating a file named [BiTeX.txt] in the root path, and paste your bibtex format citation in this .txt file.

For example, in [BiTeX.txt]:
```
@inproceedings{paper1,
  title={Title: paper1},
  author={Yuchen, Tang and AAA, AAA and BBB, BBB and CCC, CCC },
  booktitle={Proceedings of XXXXXX},
  pages={0--100},
  year={2022}
}

@inproceedings{paper2,
  title={Title: paper2},
  author={Yuchen, Tang and AAA, AAA and BBB, BBB and CCC, CCC },
  booktitle={XXX Journal},
  pages={0--100},
  year={2022}
}
...
```

Then, run ref_generate.py. A new .txt file will be generate in the root path, copy the context to your .tex file.  

The variable [ref_format] in line 5 of ref_generate.py can be changed to "CVM" or "CCDC". You can edit my code to support more journal.
