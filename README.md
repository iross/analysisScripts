makeAnalysisTrees.py
----------------
This script takes as input a root file and saves specified variables from selected events in a new root file. 

Written primarily for cutting ntuple with multiple candidates down to one candidate per event.

Usage:
```
python makeAnalysisTrees.py --file=[inputFilepath].root --out=[outputFilepath].root
```
By default, this spits out full selected trees, trees for BG estimation, trees for SS BG estimate control, and summed trees. It can take quite a while, since it's looping over all events in an incredibly inefficient way... It's possible to make the ntuples using the useLeadingOnly option to get the selected events, then run them again for the BG-like events, but this doubles the number of ntuples running around.

Example content of a processed ntuple:
```
KEY: TTree    mmeeAI_SSFinal;1        mmeeAI_SSFinal
KEY: TTree    eemmAIFinal;1   eemmAIFinal
KEY: TTree    eeeeIA_SSFinal;1        eeeeIA_SSFinal
KEY: TTree    mmmmAAFinal;1   mmmmAAFinal
KEY: TTree    eemmAAFinal;1   eemmAAFinal
KEY: TTree    eeeeIAFinal;1   eeeeIAFinal
KEY: TTree    eeeeAI_SSFinal;1        eeeeAI_SSFinal
KEY: TTree    mmmmIAFinal;1   mmmmIAFinal
KEY: TTree    mmeeAA_SSFinal;1        mmeeAA_SSFinal
KEY: TTree    eemm_oFinal;1   eemm_oFinal
KEY: TTree    mmeeFinal;1     mmeeFinal
KEY: TTree    eemmIA_SSFinal;1        eemmIA_SSFinal
KEY: TTree    mmee_oSSFinal;1 mmee_oSSFinal
KEY: TTree    eeeeFinal;1     eeeeFinal
KEY: TTree    eeeeAAFinal;1   eeeeAAFinal
KEY: TTree    eeeeAIFinal;1   eeeeAIFinal
KEY: TTree    eeee_SSFinal;1  eeee_SSFinal
KEY: TTree    eemmAI_SSFinal;1        eemmAI_SSFinal
KEY: TTree    eeeeAA_SSFinal;1        eeeeAA_SSFinal
KEY: TTree    eeeFinal;1      eeeFinal
KEY: TTree    mmmmFinal;1     mmmmFinal
KEY: TTree    mmmmAIFinal;1   mmmmAIFinal
KEY: TTree    mmmmIA_SSFinal;1        mmmmIA_SSFinal
KEY: TTree    eemmIAFinal;1   eemmIAFinal
KEY: TTree    mmeeAIFinal;1   mmeeAIFinal
KEY: TTree    eemmAA_SSFinal;1        eemmAA_SSFinal
KEY: TTree    mmmm_SSFinal;1  mmmm_SSFinal
KEY: TTree    mmee_oFinal;1   mmee_oFinal
KEY: TTree    mmeeAAFinal;1   mmeeAAFinal
KEY: TTree    mmeeIA_SSFinal;1        mmeeIA_SSFinal
KEY: TTree    eemm_oSSFinal;1 eemm_oSSFinal
KEY: TTree    mmeFinal;1      mmeFinal
KEY: TTree    mmmmAI_SSFinal;1        mmmmAI_SSFinal
KEY: TTree    eemFinal;1      eemFinal
KEY: TTree    mmmmAA_SSFinal;1        mmmmAA_SSFinal
KEY: TTree    mmeeIAFinal;1   mmeeIAFinal
KEY: TTree    mmmFinal;1      mmmFinal
KEY: TTree    llllTree;1      eeeeFinal
KEY: TTree    mmeeSumAAFinal;1        mmeeAAFinal
KEY: TTree    mmeeSumAIFinal;1        mmeeAIFinal
KEY: TTree    mmeeSumIAFinal;1        mmeeIAFinal
KEY: TTree    mmeeSumAA_SSFinal;1     mmeeAA_SSFinal
KEY: TTree    mmeeSumAI_SSFinal;1     mmeeAI_SSFinal
KEY: TTree    mmeeSumIA_SSFinal;1     mmeeIA_SSFinal
```

SkimmerClass.py
----------
Helper class used for post-processing of events.

CommonSelectors.py
-----------
Selection cut definitions.


combTrees.py
--------
Helper functions that do the 'uniquifying' of the events and provides arbitration when more than one candidate is present in an event.

analysisPlots.py
------------
Ugly macro for dumping a bunch of plots.


Differential Distributions
--------------------------
Current status: a functional mess.

Currently, the final ntuples (meaning the ones after the makeAnalysisTrees step) don't _quite_ have the variables in the way they're wanted.
So there's a quick and dirty script for getting them all shoehorned into the ntuples. The addDiffDistFriends.py script takes the file name and the trees. To the root file, it adds some friend trees which hold the 'new' variables (which are used for plotting). Any variable from the base ntuples can be plotted of course, but this was (unfortunately) the easiest way I could find to get some of the variables to work.

```
python addDiffDistFriends.py --file=DATA_test.root --trees "eeeeFinal" "mmmmFinal" "mmeeFinal" "llllTree"
```

adds the friend trees, and 

```
sh diffDist.sh
```
makes the final plots

# addDiffDistFriends.py
Adds trees containing the final variables to be plotted to the ntuple. Only necessary because the variables weren't added at ntuple creation, and I needed to hack together something that worked without having to rerun the ntuples...

# unfolding.py
Handles the unfolding (surprise!). Takes loads of arguments:
```
tree is the name of the tree to plot measured 
nice is just a nice name for plot saving purposes
vartrue is the name of the GEN truth variable (as saved in the genlevel/genEventTree in the base ntuple)
varmeas is the name of the measured variable (as saved in the xxyyFinal trees in the processed ntuple)
tmVar is the name of the truth variable (as saved in the the xxyyFinal trees in the processed ntuple... it's only used for half-implemented purity checks)
bins are self explanatory
plotname is used in the saved figure name
lumi is the integrated lumi
xTitle is the title for the x axis
xUnits is the units
legX and legY are the position of the legend
wt is the weight branch
testFile is the name of the dataset to be unfolded
```

# diffDist.sh
Actually makes the differential distributions, calling unfolding.py with all the binning/variable/etc. options.. It's all a bit messy and should be cleaned up a bit.
