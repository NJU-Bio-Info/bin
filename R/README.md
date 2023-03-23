> # deeptools2r.R

This R command tool can help you visualize the computeMatrix output, especially for the strand specific data.

## Usage:

```shell
/path/to/deeptools2r.R --help
```

```r
usage: deeptools2r.R [-h] [--version] --input INPUT [INPUT ...]
                     [--output OUTPUT]
                     [--averageType {mean,max,min,median,sum}]
                     [--plotType {line,heatmap,both}]
                     [--colors COLORS [COLORS ...]] --group GROUP [GROUP ...]
                     [--startLabel STARTLABEL] [--endLabel ENDLABEL]
                     [--refPointLabel REFPOINTLABEL] [--yMax YMAX]
                     [--yMin YMIN] [--width WIDTH] [--plotHeight PLOTHEIGHT]
                     [--plotWidth PLOTWIDTH]

This tool can help you visualize deeptools computeMatrix output in R.

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --input INPUT [INPUT ...], -i INPUT [INPUT ...]
                        the complexHeatmap output file, multiple files should
                        be separated by spaced.
  --output OUTPUT, -o OUTPUT
                        the output file name, "deeptools2r.out.pdf" by
                        default.
  --averageType {mean,max,min,median,sum}, -t {mean,max,min,median,sum}
                        the type of stastics should be used for the profile,
                        "mean" by default.
  --plotType {line,heatmap,both}
                        the plot type for profile, "line" by default.
  --colors COLORS [COLORS ...]
                        the colors used for plot lines, multiple colors should
                        be separated by spaced and should be equal with group
                        information size, "None" by default.
  --group GROUP [GROUP ...], -g GROUP [GROUP ...]
                        group information for INPUT FILE, an important
                        function of this tool is to combine profile data from
                        forward and reverse strand. For example, if you have
                        the file list: r1.fwd.tab r1.rev.tab r2.tab, you
                        should pass "-g r1_f r1_r r2" to this argument. All in
                        all, profile data from one sample but different strand
                        should be taged with same group but different strand.
  --startLabel STARTLABEL
                        [Only for scale-regions mode] Label shown in the plot
                        for the start of the region, "TSS" by default.
  --endLabel ENDLABEL   [Only for scale-regions mode] Label shown in the plot
                        for the end of the region, "TES" by default.
  --refPointLabel REFPOINTLABEL
                        [Only for reference-point mode] Label shown in the
                        plot for the center of the region
  --yMax YMAX           Maximum value for Y-axis, NA by default.
  --yMin YMIN           Minimum value for Y-axis, NA by default.
  --width WIDTH         Width value for line plot, 0.7 by default
  --plotHeight PLOTHEIGHT
                        Plot height in inch, 5 by default.
  --plotWidth PLOTWIDTH
                        Plot width in inch, 7 by default.

Kun-Ming Shui, skm@smail.nju.edu.cn
```

## Dependency

- argsparse
- ggplot2
- patchwork
- pheatmap
- tidyr
- dplyr
- purrr
- forcats

*Note: the patchwork and pheatmap are used for heatmap, which is still under development. 
If you do not want to install these two packages, you can simply delete the following commands in ```deeptools2r.R```:*

```r
suppressMessages(library(patchwork))
suppressMessages(library(pheatmap))
```

> # Example:

Input files: GRO-seq data, strand specific data

ex. Hela_1.f.txt  Hela_1 sample GRO-seq forward bigwig files computeMatrix with genes bed file from forward strand.

- Hela_1.f.txt
- Hela_1_r.txt
- Hela_2_f.txt
- Hela_2_r.txt

```shell
deeptools2r.R --input Hela_1.f.txt Hela_1.r.txt Hela_2.f.txt Hela_2.r.txt \
  --output Hela_gro.pdf \
  --colors '#a50026' '#313695' \
  --group Hela_1_f Hela_1_r Hela_2_f Hela_2_r \
  --plotHeight 4 \
  --plotWidth 5
```

![image](https://user-images.githubusercontent.com/92142596/227109389-772daf15-8ac5-4369-b7b1-5ec377814ff6.png)

> # Additional information

Due to the ggplot2 limits [click here](https://github.com/tidyverse/ggplot2/issues/2907), until now, 
if you want to specify the y-axis range, you must set ```--yMin``` and ```--yMax``` at the same time.

> # Bug Report

Feel free to create issue or email to skm@smail.nju.edu.cn.
