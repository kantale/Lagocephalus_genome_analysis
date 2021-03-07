
library(ggtree)
library(treeio)
library(tidyverse)
library(plotrix)

###############################
── Attaching packages ──────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse 1.3.0 ──
✓ ggplot2 3.3.2     ✓ purrr   0.3.4
✓ tibble  3.0.3     ✓ dplyr   1.0.4
✓ tidyr   1.1.1     ✓ stringr 1.4.0
✓ readr   1.4.0     ✓ forcats 0.5.1
── Conflicts ─────────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
x dplyr::filter() masks stats::filter()
x dplyr::lag()    masks stats::lag()
################################


tree <- read.tree("newick.txt") ##rooted

tips <- tree$tip.label
> length(tips)
> tps <- tips[tips != 'L.sceleratus']
> length(tps)


###read tree###
ggtree(tree, size = 0.5, linetype = 1) + 


#####set points for bootstrap ######
geom_point2(aes(subset=(label %in% n1),x = x - .002, colour="90-80"),size=2) + 

#####set points for bootstrap ######
geom_point2(aes(subset=(label %in% n2),x = x - .0025, ,colour="95-91"),size=2) +  

#####set points for bootstrap ######
geom_point2(aes(subset=(label %in% n3),x = x - .003,,colour="99-96"),size=2)  + 

#####set points for bootstrap ######
geom_point2(aes(subset=(label == 100), x = x - .003, ,colour="100"), size=2) + 


#####colors for bootstraps ######
scale_colour_manual(name="Bootstrap", breaks=c("100", "99-96", "95-91", "90-80"), values = c("100"="red","99-96"="deepskyblue","95-91"="magenta2","90-80"="yellow1")) +


#### change the limits of plot #####
coord_cartesian(clip = 'off') +   


#### theme tree #####
theme_tree2(plot.margin=margin(15, 70, 5, 5))  + 



##### theme for legend #####
theme(legend.position=c(0.2,0.8)) + theme(legend.background = element_rect(fill="lightblue",size=0.5, linetype="solid"))  + 



##### line grouping Tetraodontiformes #####
geom_cladelabel(node = 50, label = "Tetraodontiformes", align = TRUE, angle = -90, offset.text = .01, hjust = "center", offset = 0.1, extend = 0.6,barsize = 0.4, fontsize = 4) + 


##### tips for labels ##### (all except of L.sceleratus)
geom_tiplab(aes(subset = label %in% tps), fontface = 'italic', offset = 0.01 ) +


##### tips for labels ##### (only L.sceleratus)
geom_tiplab(aes(subset = label %in% "L.sceleratus"), fontface="bold.italic", offset = 0.01) + 


##### hilight node for Tetraodontiformes #####
geom_hilight(node = 50, fill = "#229f8a", alpha = 0.2, extend = 0.09)

