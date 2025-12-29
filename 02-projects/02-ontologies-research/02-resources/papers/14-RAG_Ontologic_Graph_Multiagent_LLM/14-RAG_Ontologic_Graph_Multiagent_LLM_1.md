<!-- Source: 14-RAG_Ontologic_Graph_Multiagent_LLM.pdf | Chunk 1/3 -->

Solar Physics
DOI: 10.1007/•••••-•••-•••-••••-•


A Statistical Study of Solar White-Light Flares
Observed by the White-light Solar Telescope of the
Lyman-alpha Solar Telescope on the Advanced
Space-based Solar Observatory (ASO-S/LST/WST)
at 360 nm


Zhichen Jing [1,2] - Ying Li [1,2] - Li Feng [1,2] Hui Li [1,2] - Yu Huang [1,2] - Youping Li [1,2] Yang Su [1,2] - Wei Chen [1,2] - Jun Tian [1,2] Dechao Song [1,2] - Jingwei Li [1] Jianchao Xue [1] - Jie Zhao [1] - Lei Lu [1] Beili Ying [1] - Ping Zhang [1] - Yingna Su [1,2] Qingmin Zhang [1,2] - Dong Li [1,2] - Yunyi Ge [1] Shuting Li [1,2] - Qiao Li [1,2] - Gen Li [1,2] Xiaofeng Liu [1,2] - Guanglu Shi [1,2] Jiahui Shan [1,2] - Zhengyuan Tian [1,2] Yue Zhou [1,2] - Weiqun Gan [1,3]


**©** The author(s) **••••**


Abstract Solar white-light flares (WLFs) are those accompanied by brightenings in the optical continuum or integrated light. The White-light Solar Telescope
(WST), as an instrument of the Lyman-alpha Solar Telescope (LST) on the
Advanced Space-based Solar Observatory (ASO-S), provides continuous solar
full-disk images at 360 nm, which can be used to study WLFs. We analyze 205
major flares above M1.0 from October 2022 to May 2023 and identify 49 WLFs
at 360 nm from WST observations, i.e. with an occurrence rate of 23.9%. The
percentages of WLFs for M1 – M4 (31 out of 180), M5 – M9 (11 out of 18), and

## � Y. Li

[yingli@pmo.ac.cn](mailto:yingli@pmo.ac.cn)


Z. C. Jing
[zcjing@pmo.ac.cn](mailto:zcjing@pmo.ac.cn)


1 Key Laboratory of Dark Matter and Space Astronomy, Purple Mountain Observatory,
Chinese Academy of Sciences, Nanjing 210023, China


2 School of Astronomy and Space Science, University of Science and Technology of China,
Hefei 230026, China


3 University of Chinese Academy of Sciences, Nanjing 211135, China


SOLA: paper.tex; 17 January 2024; 4:05; p. 1


Z. Jing et al.


above X1 (7 for all) flares are 17.2%, 61.1%, and 100%, respectively, namely the
larger the flares, the more likely they are WLFs at 360 nm. We further analyze
39 WLFs among the identified WLFs and investigate their properties such as
white-light enhancement, duration, and brightening area. It is found that the
relative enhancement of the white-light emission at 360 nm is mostly (>90%)
less than 30% and the mean enhancement is 19.4%. The WLFs’ duration at
360 nm is mostly (>80%) less than 20 minutes and its mean is 10.3 minutes.
The brightening area at 360 nm is mostly (>75%) less than 500 arcsecond [2] and
the median value is 225. We find that there exist good correlations between the
white-light enhancement/duration/area and the peak soft X-ray (SXR) flux of
the flare, with correlation coefficients of 0.68, 0.58, and 0.80, respectively. In
addition, the white-light emission in most WLFs peaks around the same time
as the temporal derivative of SXR flux as well as the hard X-ray emission at
20 – 50 keV, indicative of Neupert effect. It is also found that the limb WLFs are
more likely to have a greater enhancement, which is consistent with numerical
simulations.


Keywords: Flares, White-Light; Center-Limb Observations; X-Ray Bursts, Association with Flares


1. Introduction


Solar flares are a kind of energetic activity with sudden brightening in the solar
atmosphere (e.g. Fletcher et al., 2011; Shibata and Magara, 2011). White-light
flares (WLFs) are the flares with an enhancement in the optical continuum
or integrated light (Svestka, [ˇ] 1970; Neidig, 1989; Hudson, 2011). Although the
first flare observed in 1859 was a WLF (Carrington, 1859; Hodgson, 1859), the
number of WLFs is very small. Only about 100 WLFs were reported before 2010
(Cheng, Ding, and Carlsson, 2010). From 2011 to 2016, about 50 WLFs were
observed by the Solar Optical Telescope (SOT) on Hinode (Watanabe, Kitagawa,
and Masuda, 2017) and no more than 150 WLFs were reported using the data of
Helioseismic and Magnetic Imager (HMI) on the Solar Dynamics Observatory
(SDO) (e.g. Kuhar et al., 2016; Song and Tian, 2018; Castellanos Dur´an and
Kleint, 2020).
Many WLFs are found to have a very strong correlation with the hard Xray (HXR) and radio emissions in time and space (e.g. Hudson, Wolfson, and
Metcalf, 2006; Krucker et al., 2011). This implies that nonthermal electrons are
the source of WLFs’ energy. However, only the most energetic electrons with
more than 900 keV can reach the photosphere (Neidig, 1989) where the whitelight (WL) emission is usually emitted (e.g. Watanabe, Masuda, and Segawa,
2012), so it is hard for the nonthermal electrons to heat the photosphere directly. To resolve this problem, much effort has been made to explore the energy
transfer and radiative-heating process in the low atmosphere (e.g. Aboudarham
and Henoux, 1986a; Tian et al., 2022) and many heating sources or mechanisms for WLFs have been proposed, including electron beams (Hudson, 1972;
Aboudarham and Henoux, 1986b; Watanabe and Imada, 2020), proton beams


SOLA: paper.tex; 17 January 2024; 4:05; p. 2


A Statistical Study of WLFs Observed by WST


(Machado, Emslie, and Brown, 1978; Proch´azka, 2019), chromospheric backwarming (Machado, Emslie, and Avrett, 1989; Ding et al., 2003), soft X-ray
(SXR) irradiation (Machado, 1978), EUV irradiation (Somov and Syrovatski [˘] i,
1976), chromospheric condensations (Gan and Mauas, 1994; Gan, H´enoux, and
Fang, 2000), and Alfv´en waves (Fletcher and Hudson, 2008). In fact, the enhancement of the WL continuum during a flare is likely caused by the joint
action of several heating mechanisms (Xu et al., 2010; Song et al., 2023).
WLFs are observed not only with ground-based telescopes, but also by spacecraft that can provide detailed information. Compared with ground-based telescopes, space telescopes have better and more stable observation conditions.
The Soft X-ray Telescope (SXT) on Yohkoh can provide solar images in the
waveband at 430.8 nm with a bandwidth of ≈3 nm (Tsuneta et al., 1991). With
the SXT data, WLFs were observed from space for the first time (Hudson et al.,
1992). The Transition Region and Coronal Explorer (TRACE) has a very broad
WL channel from 170 nm to ≈1000 nm (Metcalf et al., 2003). Hinode/SOT can
provide observations at 430.5 nm with a bandwidth of 0.8 nm (Kosugi et al.,
2007). SDO/HMI gives solar full-disk images at Fe i 617.3 nm (Scherrer et al.,
2012). It should be mentioned that there had been no prior systematic imaging
observations in the Balmer continuum (i.e. below the Balmer limit at 364.6 nm)
for WLFs, at least for the wavelength range above 300 nm.
The Advanced Space-based Solar Observatory (ASO-S; Gan et al., 2023) is the
first comprehensive solar mission in China, which was launched on 9 October
2022, having a Sun-synchronous orbit with an altitude of ≈720 km. The primary
aim of ASO-S is to study the magnetic field, solar flares, coronal mass ejections,
and their relationships (Gan et al., 2019). ASO-S has three payloads: the Fulldisk vector MagnetoGraph (FMG: Su et al., 2019a), the Hard X-ray Imager
(HXI: Zhang et al., 2019; Su et al., 2019b), and the Lyman-alpha Solar Telescope
(LST: Li et al., 2019). LST consists of three scientific instruments (Chen et al.,
2019), a Solar Disk Imager (SDI), a Solar Corona Imager (SCI), and a Whitelight Solar Telescope (WST). WST can provide continuous full-disk images in the
360±2 nm waveband (Feng et al., 2019), which helps study WLFs at 360 nm, i.e.
in the Balmer continuum. Here we still call the flares with 360 nm brightenings
WLFs, the same as in Neidig and Cliver (1983).
To investigate the physical properties of the WL emission at 360 nm for large
flares, we study all the M- and X-class flares (i.e. major flares) from 12 October
2022 (when the first M-class flare was observed by WST) to 31 May 2023. 205 Mand X-class flares are collected and 49 of them (23.9%) are identified as WLFs
at 360 nm. We further analyze 39 WLFs among them in detail to investigate
the relative enhancement, duration, and brightening area of the WL emission at
360 nm. In the following, we first introduce the observational data and flare data
set in Section 2. Then we introduce the methods in Section 3. Our observational
results are presented in Section 4. The summary and discussions are given in
Section 5.


SOLA: paper.tex; 17 January 2024; 4:05; p. 3


Z. Jing et al.


2. Observational Data and Flare Data Set


ASO-S/LST/WST provides the main data in this study. WST works in the
360±2 nm waveband and has a field of view of 1.2 R⊙. The images taken by WST
have a size of 4608×4608 pixels and the pixel scale is ≈0.5 [′′] . Note that the spatial
resolution of the images (defined as full width at half maximum) is estimated to
be about 4 [′′] and the point spread function is still being under investigation. The
cadence of the images is two minutes for a routine mode while it can be as high
as one or two seconds in a burst mode. Since the burst mode of WST was under
test during the period of our flare data set, the cadence of most flare events is two
minutes. The level 2.5 data of WST are used here, which have been corrected for
dark current and flat field, as well as made North up and radiometric calibration
applied. We further use drot map.pro in the SolarSoftWare (SSW) to remove the
influence of solar rotation. It should be pointed out that the WST observations
were partially affected by Earth eclipses starting around May 2023 and some
flares lack available observations unfortunately.
Considering a strong relationship between the WL and HXR emissions in
WLFs, we also use the HXR data from ASO-S/HXI to obtain the peak time of
the HXR emission at 20 – 50 keV for the WLFs under study. HXI has an energy
range of ≈10 – 300 keV. Its spatial resolution is 3.1 [′′] and the temporal resolution
can be as high as 0.125 seconds. Note that due to the influence of the South
Atlantic Anomaly (SAA) or the radiation belt and so on, not all the WLFs at
360 nm have HXR data from HXI.
The SXR 1 – 8 [˚] A data from the Geostationary Operational Environmental
Satellite (GOES) are used in this study as well. The GOES series spacecraft
(from GOES-1 to GOES-18) have provided continuous data on solar flares since
1975. The solar X-ray irradiances in 0.5 – 4 [˚] A and 1 – 8 [˚] A are observed by the
X-ray Sensor (XRS: Hanser and Sellers, 1996) and the latter one is widely used
to define the flare magnitude from A- to X-class.
In this work, we collect 205 major flares occurring from 12 October 2022 to 31
May 2023 that have WST observations at 360 nm. There contain 198 M-class and
7 X-class flares with the class from M1.0 to X2.3. Note that there are additional
39 M-class flares observed by GOES but not well observed by WST mainly due
to Earth eclipses, which are not analyzed here. From these 205 flares, we identify
49 (23.9%) WLFs at 360 nm. In our analysis, all the 205 flares collected are used
to study the occurrence rate of WLFs at 360 nm as well as compare the SXR
duration and spatial distribution of the WLFs with non-WLFs (in Sections 4.1
and 4.2, respectively). Furthermore, for 39 out of the identified 49 WLFs, the
physical properties including relative enhancement, duration, brightening area,
and total flux of the WL emission at 360 nm are studied (in Sections 4.3 – 4.5).
In the latter, 10 WLFs near the limb are excluded because their brightenings
extend to, or overlap, the solar limb, which leads to an underestimation of the
WL area. It should be mentioned that 9 of these excluded 10 WLFs have a
longitude of larger than 85 [◦] .


SOLA: paper.tex; 17 January 2024; 4:05; p. 4


A Statistical Study of WLFs Observed by WST


3. Methods


3.1. Identification of WLFs at 360 nm


We use the intensity ratio defined as (I − I0)/Ibackground to identify a WLF (see
Figure 1d for an example WLF), where I, I0 and Ibackground are the intensity at
360 nm for a certain pixel in the flare time (i.e. the period between the GOES
start and end times of the flare as indicated in Figure 1f), the mean intensity
from the same pixel before the flare onset (30 minutes before the GOES start
time, i.e. an interval comparable to the typical duration of a flare), and the mean
intensity from a quiet-Sun region before the flare onset (same as the former one),
respectively. Note that this ratio is unaffected by the WL brightening region in
or outside the sunspot with distinct intensities. It is only affected by a selection
of the quiet-Sun region. When selecting the quiet-Sun region, we give preference
to those near the flaring active region (see the black box in Figure 1a) to avoid
or reduce the limb darkening effect at 360 nm. Note that the selected quiet-Sun
region has a size of 20 [′′] ×20 [′′], namely ≈25 times the spatial resolution of WST.
The intensity fluctuation of the quiet-Sun region is checked to be within ±2%
(i.e. the gray line in Figure 1g) for each WLF. For all the analyzed 39 WLFs,
the average level of background fluctuations is ≈1.5%, which is actually similar
to the background level of HMI (1.3%) for the 20 WLFs studied in Song et al.
(2018).
Different thresholds of the intensity ratio are used in previous studies for
WLFs. For example, a threshold of 5% was adopted for HMI WLFs at 617.3
nm (Song et al., 2018). In the present study, we firstly consider the background
fluctuations from a quiet-Sun region, i.e. within 2%. We also consider the fluctuations in the facula region around the flaring active region. In order to make
sure that the 360 nm enhancement is caused by the flare itself, we finally adopt
8% (larger than three times the background fluctuation) as the threshold after
some tests to determine a WLF at 360 nm. Note that this threshold is somewhat
strict and may have some influence on the WL emission properties, which will
be discussed in Section 5.


3.2. Calculation of the Brightening Area of WLFs at 360 nm


When the intensity ratio defined above at a flaring pixel is greater than the
threshold of 8%, the pixel will be counted in the calculation of brightening
area for the WLF (see the region marked by a yellow curve in Figures 1a –
e). We further use the morphological-opening operation for the WL brightening
region to remove the noise points (Maurya and Ambastha, 2010). Note that
the brightening area is a function of time and can be written as S1, S2, ..., Sn,
where n represents the time frame of observations. The final brightening area for
a WLF at 360 nm is defined as S = S1 - S2 - ... � Sn (see the region marked
by an orange curve in Figures 1d and e). Note that to better understand the
WL area and its relationship with some other WL parameters, here S [in units
of arcsec [2] ] is corrected for projection effect by using the heliocentric angle [θ],
i.e. S = S0/ cos(θ), where S0 is the originally measured brightening area and θ
is derived from the flare location as listed in Table 2.


SOLA: paper.tex; 17 January 2024; 4:05; p. 5


Z. Jing et al.


3.3. Definition of the Duration of WLFs at 360 nm


Firstly, we use the temporal profile of WL brightening area (i.e. the black curve
in Figure 1g) to determine the start and end times of a WLF at 360 nm. The
start time is defined as the first time when the WL brightening area is >10 pixels
after the flare onset (see the left red vertical line in Figure 1g), while the end
time is defined as the time when the brightening area becomes zero or shows no
obvious trend of decline (see the right red vertical line in Figure 1g). Note that
the end time of WL emission can be later than that of the SXR emission. Then,
the interval between the start and end times of WL emission is the duration [τ ]
of WLFs at 360 nm. Considering that the temporal resolution of most WLFs is
two minutes, τ has an uncertainty of four minutes. In addition, the peak time
of a WLF at 360 nm is defined as the time when the WL emission reaches its
maximum (as marked by the middle red vertical line in Figure 1g).


3.4. Definition of the Relative Enhancement of the WL Emission at
360 nm


The relative enhancement r of the WL emission at 360 nm at a certain pixel
is defined as r = (I − I0)/I0 (e.g. Hao et al., 2017; Castellanos Dur´an and
Kleint, 2020) as shown in Figure 1e, where I and I0 have the same meanings as
mentioned above. Note that r usually has a larger value for the penumbra/umbra
pixels compared with the pixels outside the sunspot, as the former pixels have
a relatively lower intensity. In the following analysis, we adopt two maximum
enhancements for each WLF. One is called “maximum pixel enhancement” [rp],
representing the maximum enhancement for the brightening pixels during the
flare. The other is called “maximum mean enhancement” [rm], representing the
maximum of the mean enhancement for the WL brightening region during the
flare.


3.5. An Example WLF


Figure 1 shows an example WLF with a GOES class of X1.1 on 11 February 2023.
From Figures 1a and b we can see that the identified brightening region at 360 nm
(marked by a yellow curve) is near a sunspot, which well matches the brightening
kernel at 170 nm (Figure 1c) observed by the Atmospheric Imaging Assembly
(AIA) on SDO. The selected quiet-Sun region (denoted by the black box in
Figure 1a) has an intensity fluctuation of less than ±1% as seen from Figure
1g. For this flare, the intensity-ratio map used to identify the WL brightening
(Figure 1d) looks similar to the enhancement map (Figure 1e), although the
value in the latter one is mostly larger than that from the former one. From
Figures 1f and g, it is seen that the WL emission at 360 nm (integrated over the
brightening area, i.e. S, as denoted by the orange curve in Figures 1d and e) is
synchronous with the emission at 170 nm roughly, both of which peak around the
same time as the HXR 20 – 50 keV emission and the temporal derivative of SXR
1 – 8 [˚] A, i.e. the Neupert effect (Neupert, 1968). It is also seen that the temporal
profile of WL brightening area peaks at a later time than the WL emission.


SOLA: paper.tex; 17 January 2024; 4:05; p. 6


A Statistical Study of WLFs Observed by WST


4. Results


4.1. Occurrence Rate of WLFs at 360 nm


Based on the above method, we identify 49 WLFs at 360 nm from the collected
205 M- and X-class flares, i.e. with an occurrence rate of 23.9%. We further check
the dependence of the occurrence rate on flare magnitude. As shown in Table 1,
the percentages of WLFs for M1.0 – M4.9 (31 out of 180), M5.0 – M9.9 (11 out
of 18), and above X1 (7 for all) flares are 17.2%, 61.1%, and 100%, respectively.
In other words, the larger the flares are, the more likely they are to be WLFs
at 360 nm. In particular, all the X-class flares are WLFs at 360 nm in our data
set.


Table 1. Occurrence rate of WLFs at 360 nm.


Flare class WLF non-WLF Total Occurrence rate


M1.0 – M4.9 31 149 180 17.2%
M5.0 – M9.9 11 7 18 61.1%
Above X1.0 7 0 7 100%
Total 49 156 205 23.9%


4.2. SXR Duration and Spatial Distribution of the WLFs at 360 nm
Compared with non-WLFs


Figures 2a and b show the histogram of the SXR duration (i.e. the temporal
interval between the GOES start and end times) and its scatter plot versus
peak SXR flux for all the collected major flares, in which WLFs and non-WLFs
are indicated by red and blue colors, respectively. One can see that the SXR
durations for all the flares are a few to tens of minutes. Compared with nonWLFs that have a mean SXR duration of 29.6 minutes, the WLFs tend to have
a shorter SXR duration, with a mean value of 22.5 minutes. In addition, the
WLFs tend to have a larger peak SXR flux (with a mean value of 5.26×10 [−][5] W
m [−][2] ) compared with non-WLFs (with a mean value of 1.80×10 [−][5] W m [−][2] ).
Figure 2c shows the spatial distribution on solar disk for all the collected
major flares with the WLFs and non-WLFs plotted in red and blue plus symbols,
respectively. There are 120 flares on the northern hemisphere and 32 out of them
are WLFs at 360 nm, i.e. with a percentage of 26.7%. For the remaining 85 major
flares that are located at the southern hemisphere, there are 17 WLFs at 360 nm
among them, i.e. 20%. Therefore, the spatial distribution of WLFs seems to have
no dependence on solar northern or southern hemisphere compared with nonWLFs, at least for our flare data set. However, we notice that there are many of
WLFs located near the solar limb. We further investigate the dependence of the
WLF’s distribution on solar longitude as shown in Figure 2d. It is seen that the
number of WLFs exhibits an increasing tendency, say, from several to more than
ten, from disk center to limb. Although there are more major flares occurring


SOLA: paper.tex; 17 January 2024; 4:05; p. 7


Z. Jing et al.


near the limb in our data set, the percentage of WLFs (i.e. the red curve) still
increases from ≈17% to ≈33% over the degree of longitude. This indicates that
more WLFs could take place or can be detected near the solar limb.


4.3. WL Duration, Brightening Area, and Relative Enhancement of
WLFs at 360 nm


In the following, we focus on 39 WLFs (including 6 X- and 33 M-class flares as
listed in Table 2) among the identified 49 WLFs to further study their physical
properties. Note that the other 10 WLFs are excluded here due to their brightenings extending to the solar limb, which could lead to an underestimation of
the WL area, as mentioned above.
Figure 3 shows the histogram of WLFs’ parameters including WL duration [τ ],
brightening area (S, corrected for projection effect), maximum mean enhancement [rm], and maximum pixel enhancement [rp]. The values of these parameters
are also given in Table 2. From Figure 3a we can see that most WLFs (≈85%)
have a duration of less than 20 minutes. The longest duration is 44 minutes
coming from the X2.3 WLF on 17 February 2023, i.e. the largest flare in our
data set. The mean and median durations for all the 39 WLFs are 10.3 and
7.8 minutes, respectively. From Figure 3b it is seen that most WLFs (≈75%)
have a brightening area of smaller than 500 arcsec [2] and the mean/median area
of all WLFs is 479/225 arcsec [2] . For rm and rp shown in Figures 3c and d, one
can see that most of WLFs have a rm of less than 40% and a rp of less than
75%. The mean rm and rp of all WLFs are 19.4% and 41.7%, respectively, and
the medians are 17.4% and 32.3%, respectively. Note that the X2.1 WLF on
3 March 2023 (the second largest flare in our data set) near the limb has the
largest enhancement, with a rp of 203% and a rm of 62.1%.
The relationships among the above WL parameters are further studied by
calculating their correlation coefficients (cc), as shown in Figure 4. We can see
that rm and rp of all the 39 WLFs have a strong positive correlation with cc=0.95
(see the scatter plot in Figure 4a). rm also has a good relationship with the
corrected area (cc=0.62, Figure 4b). While rm has no obvious relationship with
the WL duration (cc=0.25, Figure 4c). In addition, the WL duration has a poor
correlation with the corrected area (cc=0.33, Figure 4d).
Figure 5a shows the center-to-limb distribution (in terms of the heliocentric
angle [θ] from 0 to 90 [◦] ) of rm for all the 39 WLFs. It is seen that as θ increases,
rm reaches a higher value, though a small rm can also show up near the limb. The
cc between rm and θ for all the 39 WLFs is 0.24, i.e. showing a weak relevance.
However, if we only choose WLFs above M6.0 (see the red star symbols), there
exists a much stronger correlation (cc=0.60) between rm and θ. This suggests
that rm has a center-to-limb variation especially for large WLFs, which will be
discussed in Section 5.
In addition, we check the relationship between WL duration and SXR rise
time (i.e. the time period from flare onset to peak) for the 39 WLFs, as shown
in Figure 5b. There shows a good positive correlation (with cc=0.57) between
these two parameters. Note that the WL duration has a comparable value with


SOLA: paper.tex; 17 January 2024; 4:05; p. 8


A Statistical Study of WLFs Observed by WST


the SXR rise time. This implies that the WL emission is mainly caused by the
heating process as indicated by the SXR rise time of a flare.
The dependencies of WL parameters at 360 nm on flare magnitude or peak
SXR flux are shown in Figure 6. We can see that all the parameters, rp, rm, τ,
and S, have a good relationship with the peak SXR flux, with cc of 0.74, 0.68,
0.58 and 0.80, respectively. This is reasonable, since a larger flare tends to have
a more energy, which can lead to a stronger WL brightening.


4.4. Relationships of the WL Peak Time with SXR and HXR Peak
Times


Comparing the WL peak time to the SXR or HXR peak time can help us
understand the physical origin of WL emission in flares. Figure 7a plots the
histogram of the time difference between WL and SXR peak times for all the 39
WLFs. Note that the pink and red colors refer to the WLFs with and without
available HXR 20 – 50 keV observations from ASO-S/HXI, respectively. It is seen
that two thirds (26) of the WLFs have an earlier WL peak time compared to the
SXR peak time. Considering an uncertainty of ±2 minutes for the WL peak time,
there are still 12 WLFs (about one third) having a time difference of less than −2
minutes, while only two WLFs have that of more than two minutes. Therefore,
the WL emission tends to reach its peak earlier than the SXR emission. This also
implies that the WL emission is mainly associated with the heating process of the
flare, i.e. similar to the indications of the relationship between the WL duration
and SXR rise time as mentioned above. Note that there are two WLFs (an M4.5
and an M1.6) whose WL emissions peak much later (≈ten minutes) than the
SXR emission. These gradual-phase WL emissions might be more related to the
cooling process of the flare.
We further check the difference between the WL peak time and the peak time
of SXR temporal derivative as shown in Figure 7b. We can see that most of
the WLFs (95%) have a peak time of WL roughly the same as that of the SXR
temporal derivative, with the time difference of ±4 minutes, including all the 25
WLFs with the HXR data available (see the pink color). This indicates that the
WL emission at 360 nm exhibits the Neupert effect (Neupert, 1968) in principle.
The two exceptional WLFs are those having a later WL peak time as mentioned
before. They also have a later WL peak time than the one of SXR temporal
derivative.
For the 25 WLFs with HXR data available, we further plot the histogram
of the difference between WL and HXR peak times in Figure 7c. One can see
that all these WLFs have a similar peak time for the WL and HXR emissions
within a range of ±4 minutes and particularly most (92%) are in the range of
±2 minutes. This confirms that the WL emission at 360 nm basically follows the
Neupert effect and thus implies that the 360 nm emission is closely related to
nonthermal electron-beam heating, at least for most WLFs under study.


4.5. Total Flux of WLFs at 360 nm



To describe the absolute enhancement of WLFs at 360 nm, we define the total

        
flux (or total energy) as: F = [�] (I − I0) (Castellanos Dur´an and Kleint,







t



(I − I0) (Castellanos Dur´an and Kleint,
St



SOLA: paper.tex; 17 January 2024; 4:05; p. 9


Z. Jing et al.



2020), i.e. integrating the enhanced WL intensity over corrected area [St] and
time [t]. Note that here the WL intensities of I and I0 have been calibrated into a
physical unit of erg s [−][1] cm [−][2] sr [−][1] . In addition, the limb-darkening effect at 360
nm has been corrected by using an empirical formula of I(Iµ(=1)µ) [=][ u][λ][+(1][−][u][λ][)][µ][+]



vλµ ln µ2+1µ [+][ w][λ][µ][(][µ][ ln][ µ][+1] µ



vλµ ln µ+1 [+][ w][λ][µ][(][µ][ ln][ µ] µ - ln 2), where uλ, vλ, and wλ are 0.2887, 2.2194, and

−5.6933, respectively (Makarova, Roshchina, and Sarychev, 1991). This formula
can fit the WST data quite well when µ > 0.11. It should be mentioned that all
the analyzed 39 WLFs have µ ≥ 0.13. The final F is listed in Table 2. It is seen
that the total flux at 360 nm with a bandwidth of ±2 nm for all the 39 WLFs
is about 10 [26] - 10 [30] erg. The relationships between the total flux and peak SXR
flux (or flare magnitude), brightening area, WL duration, and maximum mean
relative enhancement are shown in Figure 8. We can see that the total flux has a
good positive correlation with these four parameters in general, with cc of 0.89,
0.89, 0.45, and 0.73, respectively. This result is reasonable and can be predicted.
Here we also give the expression of F based on the linear fitting (see each of the
panels), which could be used to estimate the radiated energy at 360±2 nm via
the peak SXR flux only and further estimate the other WL parameters at 360
nm roughly.



5. Summary and Discussions


In this article, we present a statistical study on the WLFs at 360 nm observed
by ASO-S/WST from October 2022 to May 2023. The occurrence rate of WLFs
and comparisons between WLFs and non-WLFs are provided. The WLFs’ parameters including relative enhancement (rm and rp), WL duration, brightening
area, and total flux are given, together with their mutual relationships. The WL
peak time is also compared to the SXR and HXR peak times, which is helpful
to understand the physical origin of WL emission. Our results are summarized
below.


1. The occurrence rate of WLFs at 360 nm is 23.9% for major flares above M1.0,
which increases over the flare magnitude. It should be mentioned that all the
seven X-class flares in our data set are WLFs at 360 nm.
2. Compared with non-WLFs, the WLFs at 360 nm tend to have a shorter SXR
duration and a larger peak SXR flux. The spatial distribution of WLFs seems
to have no dependence on solar northern or southern hemisphere, at least for
our flare data set. However, the number of WLFs increases from disk center
to limb and the relative enhancement of WL emission can be larger for the
WLFs near the limb.
3. The mean values of WL duration, brightening area, rm, and rp of WLFs at
360 nm are 10.3 minutes, 479 arcsec [2], 19.4%, and 41.7%, respectively. rm is
found to have a strong relevance with rp and some positive relevance with
the area. However, it has no obvious relevance with the duration. In addition,
there is no obvious correlation between the duration and area.
4. All the WL parameters, including the duration, area, rp, rm and total flux,
show a good positive relationship with the peak SXR flux.


SOLA: paper.tex; 17 January 2024; 4:05; p. 10


A Statistical Study of WLFs Observed by WST


5. The WL emission at 360 nm reaches its peak around the same time as the
temporal derivative of SXR flux as well as the HXR 20 – 50 keV emission
for most WLFs. This indicates that the WL emission basically follows the
Neupert effect. It should be noted that there are two WLFs showing a notable
gradual-phase emission at 360 nm.
6. The total flux at 360 nm for the 39 WLFs under study is about 10 [26] - 10 [30] erg.
It has a good positive correlation with the peak SXR flux, WL enhancement,
and brightening area.


Our study presents a continuous observation of major flares at 360 nm for
more than half a year from ASO-S/WST as well as provides the occurrence rate
of WLFs at 360 nm for the first time. Although there are some other telescopes
observing the Sun in the 360 nm waveband, such as the Optical and Near-infrared
Solar Eruption Tracer (ONSET: Fang et al., 2013), the advantages of WST are
the continuity of its observation in a seeing-free condition from space and its
full-disk field of view being beneficial for flare studies. Nearly 50 WLFs have
been identified in the period of less than one year, which is roughly equivalent
to the number of WLFs observed by HMI at 617 nm for about 2 – 3 years. Note
that our threshold for identifying a WLFs at 360 nm is relatively high and the
burst mode of WST for a very high cadence was still under test. Therefore, there
should be more WLFs detected by WST during this period. Here we should also
mention that WST and HMI work in different wavebands and the occurrence
rate of WLFs in these two wavebands can be different.
Based on some statistical studies on HMI WLFs at 617 nm in the literature,
here we can roughly compare the properties of WL emissions between WST 360
nm and HMI 617 nm. For instance, the mean enhancement of the emission at 617
nm is ≈15% (e.g. Song et al., 2018, Castellanos Dur´an and Kleint, 2020), and
rm of the emission at 360 nm is ≈19%. Considering that a higher threshold of
intensity ratio for WLFs, i.e. 8% in the present study, would overestimate a rm,
we may say that the mean enhancement at 360 nm is comparable to that at 617
nm in WLFs. In addition, the duration and area of WLFs at 617 nm have median
values of ≈5 minutes and <50 arcsec [2] (without a correction of project effect;
Song et al., 2018), respectively, both of which are smaller than those of WLFs at
360 nm. Note that a higher threshold for WLFs here would underestimate the
brightening area and duration of the emission at 360 nm. A detailed comparison
between the emissions at WST 360 nm (in the Balmer continuum) and HMI 617
nm (in the Paschen continuum) deserves a further study for WLFs. In fact, the
relationship between the 360 nm emission and the emission at >400 nm, i.e. the
true WL, is worthwhile to be explored.
In the present study, the WL emission at 360 nm reaches its peak around
the same time as the temporal derivative of the SXR 1 – 8 [˚] A flux as well as
the HXR 20 – 50 keV emission in most WLFs, i.e. exhibiting the Neupert effect.
This suggests that the 360 nm emission can be closely related to a nonthermal
electron beam heating, i.e. having a nonthermal origin. It should be noted that
there are two exceptional WLFs in our data set, whose emissions at 360 nm have
a later peak time than the SXR 1 – 8 [˚] A flux. This kind of emission appearing in
the decay phase of the flare (or gradual-phase emissions) might be produced by


SOLA: paper.tex; 17 January 2024; 4:05; p. 11


Z. Jing et al.


a thermal process (say, thermal conduction or SXR backwarming) rather than a
nonthermal electron-beam heating that usually occurs in the rise phase. These
are worthy of a detailed study in the future.
In our study, the WL emission at 360 nm exhibits a center-to-limb variation,
which is manifested as a larger enhancement plus more WLFs identified near
the limb. This is consistent with previous studies on WL emission both in
observations and numerical simulations. A statistical work on 86 WLFs showed
that the WLFs prefer to occur at the solar limb (Neidig, Wiborg, and Gilliam,
1993). Some numerical simulations revealed that the electron-beam heating leads
to a larger enhancement in the continuum near the solar limb than at the disk
center (e.g. Ding, 2007; Cheng, Ding, and Carlsson, 2010). The authors gave
an explanation that the formation height of continuum emission is higher in
limb flares and it is easier to heat. Our study provides an observational evidence
for the center-to-limb effect of the 360 nm emission from a statistical analysis.
Furthermore, we find that the center-to-limb variation is more obvious for larger
WLFs.
At the time of writing, WST is beginning to provide WL images with a very
rapid cadence of one or two seconds in a burst mode. This can bring some new
sights on WLFs at 360 nm. Firstly, a high temporal resolution can provide precise
start, peak, and end times of WL emission as well as their relationships with
the corresponding times of SXR and HXR emissions, which helps understand the
physical origin of the 360 nm emission. A rapid cadence of WL images might also
make it possible to detect WL waves at 360 nm accompanied by WLFs (like sunquakes observed from HMI; Wu, Dai, and Ding, 2023). This would be very helpful
to explore the conditions in the WL emission source. As more and more WLFs
are collected from WST observations, it is worthwhile doing a comprehensive
statistical work combining with the data from some other instruments such as
HMI, ONSET, and the Chinese Hα Solar Explorer (CHASE: Li et al., 2022). On
the other hand, radiative-hydrodynamic simulations are needed to help explain
the observations in terms of formation height and contribution function of the
WL emission. All these should improve our understanding of WLFs at 360 nm.


Acknowledgments The authors thank the reviewer very much for the valuable, as well as,


detailed suggestions and comments that helped to improve the manuscript greatly. The ASO-S


mission is supported by the Strategic Priority Research Program on Space Science, Chinese


Academy of Sciences. SDO is a mission for NASA’s Living With a Star program.


Author Contributions Z.C. Jing analyzed the data and wrote the first manuscript. Y. Li
proposed the initial idea, helped the data analysis, and revised the manuscript. J. Tian and
D.C. Song provided suggestions on the data analysis. W.Q. Gan is PI of ASO-S. H. Li and L.
Feng are PI and Co-PI of LST, respectively. Y. Huang, Y.P. Li, J.W. Li, J.C. Xue, J. Zhao,
L. Lu, B.L. Ying, P. Zhang, Y.N. Su, Q.M. Zhang, D. Li, Y.Y. Ge, S.T. Li, Q. Li, G. Li, X.F.
Liu, G.L. Shi, J.H. Shan, Z.Y. Tian, and Y. Zhou contributed on the pipeline and release of
WST data. Y. Su and W. Chen provided the HXI data. All authors reviewed the manuscript.


Funding The authors are supported by the Strategic Priority Research Program of the Chinese Academy of Sciences (Grant No. XDB0560000), the National Natural Science Foundation
of China (Grant Nos. 12273115, 12233012, and 11921003), and the Ministry of Science and
Technology of China (Grant No. 2022YFF0503004).


SOLA: paper.tex; 17 January 2024; 4:05; p. 12


A Statistical Study of WLFs Observed by WST


Data Availability Data of ASO-S before 1 April 2023 are under test and not publicly
available, but they are available from the corresponding author on reasonable request. Data
of ASO-S after 1 April 2023 are publicly available and can be downloaded from the official
[website of ASO-S at aso-s.pmo.ac.cn/sodc/dataArchive.jsp. Data of SDO used in this work are](http://aso-s.pmo.ac.cn/sodc/dataArchive.jsp)
[publicly available at jsoc.stanford.edu.](http://jsoc.stanford.edu)


Declarations


Conflict of interest The authors declare no competing interests.


References


Aboudarham, J., Henoux, J.C.: 1986a, Energy deposit at temperature minimum level and
[white light flares. Astron. Astrophys. 156, 73. ADS.](https://ui.adsabs.harvard.edu/abs/1986A&A...156...73A)
Aboudarham, J., Henoux, J.C.: 1986b, Non-thermal excitation and ionization of hydrogen in
[solar flares. I. Effects on a flaring chromosphere. Astron. Astrophys. 168, 301. ADS.](https://ui.adsabs.harvard.edu/abs/1986A&A...168..301A)
Carrington, R.C.: 1859, Description of a Singular Appearance seen in the Sun on September
[1, 1859. Mon. Not. R. Astron. Soc. 20, 13. DOI. ADS.](https://doi.org/10.1093/mnras/20.1.13)
Castellanos Dur´an, J.S., Kleint, L.: 2020, The Statistical Relationship between White-light
[Emission and Photospheric Magnetic Field Changes in Flares. Astrophys. J. 904, 96. DOI.](https://doi.org/10.3847/1538-4357/ab9c1e)
[ADS.](https://ui.adsabs.harvard.edu/abs/2020ApJ...904...96C)
Chen, B., Li, H., Song, K.-F., Guo, Q.-F., Zhang, P.-J., He, L.-P., Dai, S., Wang, X.-D., Wang,
H.-F., Liu, C.-L., Zhang, H.-J., Zhang, G., Wang, Y., Liu, S.-J., Zhang, H.-X., Liu, L., Mao,
S.-L., Liu, Y., Peng, J.-H., Wang, P., Sun, L., Liu, Y., Han, Z.-W., Wang, Y.-L., Wu, K.,
Ding, G.-X., Zhou, P., Zheng, X., Xia, M.-Y., Wu, Q.-W., Xie, J.-J., Chen, Y., Song, S.-M.,
Wang, H., Zhu, B., Chu, C.-B., Yang, W.-G., Feng, L., Huang, Y., Gan, W.-Q., Li, Y., Li,
J.-W., Lu, L., Xue, J.-C., Ying, B.-L., Sun, M.-Z., Zhu, C., Bao, W.-M., Deng, L., Yin,
Z.-S.: 2019, The Lyman-alpha Solar Telescope (LST) for the ASO-S mission - II. design of
[LST. Res. Astron. Astrophys. 19, 159. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/159)
Cheng, J.X., Ding, M.D., Carlsson, M.: 2010, Radiative Hydrodynamic Simulation of the
[Continuum Emission in Solar White-Light Flares. Astrophys. J. 711, 185. DOI. ADS.](https://doi.org/10.1088/0004-637X/711/1/185)
Ding, M.D.: 2007, The Origin of Solar White-Light Flares. In: Heinzel, P., Dorotoviˇc, I., Rutten,
R.J. (eds.) The Physics of Chromospheric Plasmas, Astron. Soc. Pacific, CS-368, San
[Francisco, 417. ADS.](https://ui.adsabs.harvard.edu/abs/2007ASPC..368..417D)
Ding, M.D., Liu, Y., Yeh, C.-T., Li, J.P.: 2003, Interpretation of the infrared continuum in a
[solar white-light flare. Astron. Astrophys. 403, 1151. DOI. ADS.](https://doi.org/10.1051/0004-6361:20030428)
Fang, C., Chen, P.-F., Li, Z., Ding, M.-D., Dai, Y., Zhang, X.-Y., Mao, W.-J., Zhang, J.-P.,
Li, T., Liang, Y.-J., Lu, H.-T.: 2013, A new multi-wavelength solar telescope: Optical and
[Near-infrared Solar Eruption Tracer (ONSET). Res. Astron. Astrophys. 13, 1509. DOI.](https://doi.org/10.1088/1674-4527/13/12/011)
[ADS.](https://ui.adsabs.harvard.edu/abs/2013RAA....13.1509F)
Feng, L., Li, H., Chen, B., Li, Y., Susino, R., Huang, Y., Lu, L., Ying, B.-L., Li, J.-W., Xue,
J.-C., Yang, Y.-T., Hong, J., Li, J.-P., Zhao, J., Gan, W.-Q., Zhang, Y.: 2019, The Lymanalpha Solar Telescope (LST) for the ASO-S mission - III. data and potential diagnostics.
[Res. Astron. Astrophys. 19, 162. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/162)
Fletcher, L., Hudson, H.S.: 2008, Impulsive Phase Flare Energy Transport by Large-Scale
[Alfv´en Waves and the Electron Acceleration Problem. Astrophys. J. 675, 1645. DOI. ADS.](https://doi.org/10.1086/527044)
Fletcher, L., Dennis, B.R., Hudson, H.S., Krucker, S., Phillips, K., Veronig, A., Battaglia, M.,
Bone, L., Caspi, A., Chen, Q., Gallagher, P., Grigis, P.T., Ji, H., Liu, W., Milligan, R.O.,
Temmer, M.: 2011, An Observational Overview of Solar Flares. Space Sci. Rev. 159, 19.
[DOI. ADS.](https://doi.org/10.1007/s11214-010-9701-8)
Gan, W.Q., Mauas, P.J.D.: 1994, Atmospheric Heating in Solar Flares by Chromospheric
[Condensation. Astrophys. J. 430, 891. DOI. ADS.](https://doi.org/10.1086/174459)
Gan, W.Q., H´enoux, J.C., Fang, C.: 2000, On the origin of solar white-light flares. Astron.
[Astrophys. 354, 691. ADS.](https://ui.adsabs.harvard.edu/abs/2000A&A...354..691G)
Gan, W.-Q., Ding, M.-D., Huang, Y., Su, Y.-N.: 2019, Preface: Advanced Space-based Solar
[Observatory (ASO-S). Res. Astron. Astrophys. 19, 155. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/155)


SOLA: paper.tex; 17 January 2024; 4:05; p. 13


Z. Jing et al.


Gan, W., Zhu, C., Deng, Y., Zhang, Z., Chen, B., Huang, Y., Deng, L., Wu, H., Zhang, H.,
Li, H., Su, Y., Su, J., Feng, L., Wu, J., Cui, J., Wang, C., Chang, J., Yin, Z., Xiong, W.,
Chen, B., Yang, J., Li, F., Lin, J., Hou, J., Bai, X., Chen, D., Zhang, Y., Hu, Y., Liang,
Y., Wang, J., Song, K., Guo, Q., He, L., Zhang, G., Wang, P., Bao, H., Cao, C., Bai, Y.,
Chen, B., He, T., Li, X., Zhang, Y., Liao, X., Jiang, H., Li, Y., Su, Y., Lei, S., Chen, W.,
Li, Y., Zhao, J., Li, J., Ge, Y., Zou, Z., Hu, T., Su, M., Ji, H., Gu, M., Zheng, Y., Xu, D.,
Wang, X.: 2023, The Advanced Space-Based Solar Observatory (ASO-S). Sol. Phys. 298,
[68. DOI. ADS.](https://doi.org/10.1007/s11207-023-02166-x)
Hanser, F.A., Sellers, F.B.: 1996, Design and calibration of the GOES-8 solar x-ray sensor:
the XRS. In: Washwell, E.R. (ed.) GOES-8 and Beyond, Soc. Photo-Opt. Instrum. Eng.
[(SPIE), CS-2812, 344. DOI. ADS.](https://doi.org/10.1117/12.254082)
Hao, Q., Yang, K., Cheng, X., Guo, Y., Fang, C., Ding, M.D., Chen, P.F., Li, Z.: 2017, A
circular white-light flare with impulsive and gradual white-light kernels. Nature Comm. 8,
[2202. DOI. ADS.](https://doi.org/10.1038/s41467-017-02343-0)
Hodgson, R.: 1859, On a curious Appearance seen in the Sun. Mon. Not. R. Astron. Soc. 20,
[15. DOI. ADS.](https://doi.org/10.1093/mnras/20.1.15)
[Hudson, H.S.: 1972, Thick-Target Processes and White-Light Flares. Sol. Phys. 24, 414. DOI.](https://doi.org/10.1007/BF00153384)

[ADS.](https://ui.adsabs.harvard.edu/abs/1972SoPh...24..414H)
[Hudson, H.S.: 2011, Global Properties of Solar Flares. Space Sci. Rev. 158, 5. DOI. ADS.](https://doi.org/10.1007/s11214-010-9721-4)
Hudson, H.S., Wolfson, C.J., Metcalf, T.R.: 2006, White-Light Flares: A TRACE/RHESSI
[Overview. Sol. Phys. 234, 79. DOI. ADS.](https://doi.org/10.1007/s11207-006-0056-y)
Hudson, H.S., Acton, L.W., Hirayama, T., Uchida, Y.: 1992, White-Light Flares Observed by
[YOHKOH. Publ. Astron. Soc. Japan 44, L77. ADS.](https://ui.adsabs.harvard.edu/abs/1992PASJ...44L..77H)
Kosugi, T., Matsuzaki, K., Sakao, T., Shimizu, T., Sone, Y., Tachikawa, S., Hashimoto, T.,
Minesugi, K., Ohnishi, A., Yamada, T., Tsuneta, S., Hara, H., Ichimoto, K., Suematsu, Y.,
Shimojo, M., Watanabe, T., Shimada, S., Davis, J.M., Hill, L.D., Owens, J.K., Title, A.M.,
Culhane, J.L., Harra, L.K., Doschek, G.A., Golub, L.: 2007, The Hinode (Solar-B) Mission:
[An Overview. Sol. Phys. 243, 3. DOI. ADS.](https://doi.org/10.1007/s11207-007-9014-6)
Krucker, S., Hudson, H.S., Jeffrey, N.L.S., Battaglia, M., Kontar, E.P., Benz, A.O., Csillaghy,
A., Lin, R.P.: 2011, High-resolution Imaging of Solar Flare Ribbons and Its Implication on
[the Thick-target Beam Model. Astrophys. J. 739, 96. DOI. ADS.](https://doi.org/10.1088/0004-637X/739/2/96)
Kuhar, M., Krucker, S., Mart´ınez Oliveros, J.C., Battaglia, M., Kleint, L., Casadei, D., Hudson,
H.S.: 2016, Correlation of Hard X-Ray and White Light Emission in Solar Flares. Astrophys.
[J. 816, 6. DOI. ADS.](https://doi.org/10.3847/0004-637X/816/1/6)
Li, C., Fang, C., Li, Z., Ding, M., Chen, P., Qiu, Y., You, W., Yuan, Y., An, M., Tao, H.,
Li, X., Chen, Z., Liu, Q., Mei, G., Yang, L., Zhang, W., Cheng, W., Chen, J., Chen, C.,
Gu, Q., Huang, Q., Liu, M., Han, C., Xin, H., Chen, C., Ni, Y., Wang, W., Rao, S., Li,
H., Lu, X., Wang, W., Lin, J., Jiang, Y., Meng, L., Zhao, J.: 2022, The Chinese Hα Solar
Explorer (CHASE) mission: An overview. Science China Phys. Mech. Astron. 65, 289602.
[DOI. ADS.](https://doi.org/10.1007/s11433-022-1893-3)
Li, H., Chen, B., Feng, L., Li, Y., Huang, Y., Li, J.-W., Lu, L., Xue, J.-C., Ying, B.-L., Zhao,
J., Yang, Y.-T., Gan, W.-Q., Fang, C., Song, K.-F., Wang, H., Guo, Q.-F., He, L.-P., Zhu,
B., Zhu, C., Deng, L., Bao, H.-C., Cao, C.-X., Yang, Z.-G.: 2019, The Lyman-alpha Solar
Telescope (LST) for the ASO-S mission — I. Scientific objectives and overview. Res. Astron.
[Astrophys. 19, 158. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/158)
Machado, M.E.: 1978, Soft X-Ray Emission and Chromospheric Flares. Sol. Phys. 60, 341.

[DOI. ADS.](https://doi.org/10.1007/BF00156534)
Machado, M.E., Emslie, A.G., Avrett, E.H.: 1989, Radiative Backwarming in White-Light
[Flares. Sol. Phys. 124, 303. DOI. ADS.](https://doi.org/10.1007/BF00156272)
Machado, M.E., Emslie, A.G., Brown, J.C.: 1978, The structure of the temperature minimum
region in solar flares and its significance for flare heating mechanisms. Sol. Phys. 58, 363.
[DOI. ADS.](https://doi.org/10.1007/BF00157282)
Makarova, E.A., Roshchina, E.M., Sarychev, A.P.: 1991, Average Data on Solar Limb
[Darkening in the 300-NM to 2400-NM Quasicontinuum. Soviet Astron. 35, 441. ADS.](https://ui.adsabs.harvard.edu/abs/1991SvA....35..441M)
Maurya, R.A., Ambastha, A.: 2010, A Technique for Automated Determination of Flare Ribbon
[Separation and Energy Release. Sol. Phys. 262, 337. DOI. ADS.](https://doi.org/10.1007/s11207-009-9488-5)
Metcalf, T.R., Alexander, D., Hudson, H.S., Longcope, D.W.: 2003, TRACE and Yohkoh
[Observations of a White-Light Flare. Astrophys. J. 595, 483. DOI. ADS.](https://doi.org/10.1086/377217)
[Neidig, D.F.: 1989, The Importance of Solar White-Light Flares. Sol. Phys. 121, 261. DOI.](https://doi.org/10.1007/BF00161699)

[ADS.](https://ui.adsabs.harvard.edu/abs/1989SoPh..121..261N)


SOLA: paper.tex; 17 January 2024; 4:05; p. 14


A Statistical Study of WLFs Observed by WST


Neidig, D.F., Cliver, E.W.: 1983, The Occurrence Frequency of White Light Flares. Sol. Phys.
[88, 275. DOI. ADS.](https://doi.org/10.1007/BF00196192)
Neidig, D.F., Wiborg, P.H., Gilliam, L.B.: 1993, Physical properties of white-light flares derived
[from their center-to-limb distribution. Sol. Phys. 144, 169. DOI. ADS.](https://doi.org/10.1007/BF00667990)
Neupert, W.M.: 1968, Comparison of Solar X-Ray Line Emission with Microwave Emission
[during Flares. Astrophys. J. Lett. 153, L59. DOI. ADS.](https://doi.org/10.1086/180220)
Proch´azka, O.: 2019, Analysis and Modelling of a Type II White-light Solar Flare. PhD thesis,
[Queen’s University Belfast. DOI. ADS.](https://doi.org/10.13140/RG.2.2.29683.17442)
Scherrer, P.H., Schou, J., Bush, R.I., Kosovichev, A.G., Bogart, R.S., Hoeksema, J.T., Liu, Y.,
Duvall, T.L., Zhao, J., Title, A.M., Schrijver, C.J., Tarbell, T.D., Tomczyk, S.: 2012, The
Helioseismic and Magnetic Imager (HMI) Investigation for the Solar Dynamics Observatory
[(SDO). Sol. Phys. 275, 207. DOI. ADS.](https://doi.org/10.1007/s11207-011-9834-2)
Shibata, K., Magara, T.: 2011, Solar Flares: Magnetohydrodynamic Processes. Liv. Reviews
[in Solar Physics 8, 6. DOI. ADS.](https://doi.org/10.12942/lrsp-2011-6)
Somov, B.V., Syrovatski [˘] i, S.I.: 1976, REVIEWS OF TOPICAL PROBLEMS: Physical pro[cesses in the solar atmosphere associated with flares. Sov. Phys. Usp. 19, 813. DOI.](https://doi.org/10.1070/PU1976v019n10ABEH005337)
[ADS.](https://ui.adsabs.harvard.edu/abs/1976SvPhU..19..813S)
Song, D.-C., Tian, J., Li, Y., Ding, M.D., Su, Y., Yu, S., Hong, J., Qiu, Y., Rao, S., Liu, X.,
Li, Q., Chen, X., Li, C., Fang, C.: 2023, Spectral Observations and Modeling of a Solar
[White-light Flare Observed by CHASE. Astrophys. J. Lett. 952, L6. DOI. ADS.](https://doi.org/10.3847/2041-8213/ace18c)
Song, Y., Tian, H.: 2018, Investigation of White-light Emission in Circular-ribbon Flares.
[Astrophys. J. 867, 159. DOI. ADS.](https://doi.org/10.3847/1538-4357/aae5d1)
Song, Y.L., Tian, H., Zhang, M., Ding, M.D.: 2018, Observations of white-light flares in NOAA
active region 11515: high occurrence rate and relationship with magnetic transients. Astron.
[Astrophys. 613, A69. DOI. ADS.](https://doi.org/10.1051/0004-6361/201731817)
Su, J.-T., Bai, X.-Y., Chen, J., Guo, J.-J., Liu, S., Wang, X.-F., Xu, H.-Q., Yang, X., Song, Y.L., Deng, Y.-Y., Ji, K.-F., Deng, L., Huang, Y., Li, H., Gan, W.-Q.: 2019a, Data reduction
[and calibration of the FMG onboard ASO-S. Res. Astron. Astrophys. 19, 161. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/161)
Su, Y., Liu, W., Li, Y.-P., Zhang, Z., Hurford, G.J., Chen, W., Huang, Y., Li, Z.-T., Jiang,
X.-K., Wang, H.-X., Xia, F.-X.-Y., Chen, C.-X., Yu, W.-H., Yu, F., Wu, J., Gan, W.-Q.:
2019b, Simulations and software development for the Hard X-ray Imager onboard ASO-S.
[Res. Astron. Astrophys. 19, 163. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/163)
Tian, J., Hong, J., Li, Y., Ding, M.D.: 2022, An evaluation of different recipes for chromospheric
[radiative losses in solar flares. Astron. Astrophys. 668, A96. DOI. ADS.](https://doi.org/10.1051/0004-6361/202244615)
Tsuneta, S., Acton, L., Bruner, M., Lemen, J., Brown, W., Caravalho, R., Catura, R., Freeland,
S., Jurcevich, B., Morrison, M., Ogawara, Y., Hirayama, T., Owens, J.: 1991, The Soft X-ray
[Telescope for the SOLAR-A mission. Sol. Phys. 136, 37. DOI. ADS.](https://doi.org/10.1007/BF00151694)
ˇSvestka, Z.: 1970, The Phase of Particle Acceleration in the Flare Development. Sol. Phys. 13,
[471. DOI. ADS.](https://doi.org/10.1007/BF00153567)
Watanabe, K., Imada, S.: 2020, White-light Emission and Chromospheric Response by an
[X1.8-class Flare on 2012 October 23. Astrophys. J. 891, 88. DOI. ADS.](https://doi.org/10.3847/1538-4357/ab711b)
Watanabe, K., Kitagawa, J., Masuda, S.: 2017, Characteristics that Produce White-light
[Enhancements in Solar Flares Observed by Hinode/SOT. Astrophys. J. 850, 204. DOI.](https://doi.org/10.3847/1538-4357/aa9659)
[ADS.](https://ui.adsabs.harvard.edu/abs/2017ApJ...850..204W)
Watanabe, K., Masuda, S., Segawa, T.: 2012, Hinode Flare Catalogue. Sol. Phys. 279, 317.

[DOI. ADS.](https://doi.org/10.1007/s11207-012-9983-y)
Wu, H., Dai, Y., Ding, M.D.: 2023, Highly Energetic Electrons Accelerated in Strong Solar
[Flares as a Preferred Driver of Sunquakes. Astrophys. J. Lett. 943, L6. DOI. ADS.](https://doi.org/10.3847/2041-8213/acb0d1)
Xu, Y., Cao, W., Jing, J., Wang, H.: 2010, High resolution observations of white-light emissions
[from the opacity minimum during an X-class flare. Astron. Nach. 331, 596. DOI. ADS.](https://doi.org/10.1002/asna.201011381)
Zhang, Z., Chen, D.-Y., Wu, J., Chang, J., Hu, Y.-M., Su, Y., Zhang, Y., Wang, J.-P., Liang,
Y.-M., Ma, T., Guo, J.-H., Cai, M.-S., Zhang, Y.-Q., Huang, Y.-Y., Peng, X.-Y., Tang, Z.B., Zhao, X., Zhou, H.-H., Wang, L.-G., Song, J.-X., Ma, M., Xu, G.-Z., Yang, J.-F., Lu, D.,
He, Y.-H., Tao, J.-Y., Ma, X.-L., Lv, B.-G., Bai, Y.-P., Cao, C.-X., Huang, Y., Gan, W.-Q.:
2019, Hard X-ray Imager (HXI) onboard the ASO-S mission. Res. Astron. Astrophys. 19,
[160. DOI. ADS.](https://doi.org/10.1088/1674-4527/19/11/160)


SOLA: paper.tex; 17 January 2024; 4:05; p. 15


Z. Jing et al.


Table 2. The 39 WLFs analyzed in detail.


Observation Flare GOES GOES HXR WL WL WL WL WL WL WL WL
Date Location [1] Class Peak Peak [2] Start Peak End τ [3] rp rm S [4] F [5]

[UT] [UT] [UT] [UT] [UT] [minute] [%] [%] [arcsec [2] ] [erg]


07.11.2022 N12E56 M5.2 00:11 00:05 00:07 00:07 00:13 6.0 16.9 9.94 404±20 (5.33±0.09)×10 [26]

14.12.2022 S21W48 M4.5 22:06  - 22:07 22:15 22:39 32 24.6 13.8 194±6.4 (1.71±0.03)×10 [29]

16.12.2022 S21W64 M3.5 02:01  - 01:40 01:54 01:48 8.0 25.8 15.2 225±10 (4.22±0.07)×10 [28]

16.12.2022 S20W68 M4.0 10:19 10:18 10:16 10:20 10:36 20 28.7 17.0 233±30 (5.40±0.08)×10 [28]

30.12.2022 N20E07 M3.7 19:38 19:37 19:36 19:36 19:36 <2.0 10.9 9.47 13.0±0.65 (8.04±0.13)×10 [26]

09.01.2023 N24E79 X1.9 18:50  - 18:46 18:50 19:02 16 101 31.9 (2.62±0.33)×10 [3] (1.91±0.03) ×10 [30]

10.01.2023 S13E71 M5.1 00:16 00:14 00:14 00:14 00:24 10 34.7 18.1 (1.65±0.32)×10 [3] (2.62±0.06)×10 [29]

10.01.2023 S12E68 M1.0 02:16 02:13 02:14 02:16 02:18 4.0 23.0 12.8 163±19 (1.95±0.03)×10 [28]

10.01.2023 S13E59 M1.2 17:48 17:47 17:48 17:48 17:48 <2.0 30.6 20.3 68.9±6.0 (5.92±0.10)×10 [27]

10.01.2023 N22E62 X1.0 22:47  - 22:46 22:48 23:00 14 83.1 31.8 720±92 (3.28±0.06)×10 [29]

11.01.2023 N25E56 M2.4 00:59  - 00:52 00:54 01:10 18 16.0 10.4 176±19 (1.41±0.02)×10 [28]

11.01.2023 S13E53 M5.6 01:56 01:53 01:54 01:54 01:58 4.0 34.2 17.6 410±21 (4.97±0.08)×10 [28]

11.01.2023 N22E56 M3.1 08:33  - 08:32 08:34 08:38 6.0 71.9 24.8 276±6.3 (5.42±0.10)×10 [28]

12.01.2023 N23E49 M1.6 06:50  - 06:56 07:00 07:06 10 21.1 12.5 127±7.2 (1.03±0.02)×10 [28]

13.01.2023 S11W83 M4.0 10:15  - 10:13 10:13 10:15 2.0 33.1 17.4 (1.59±0.33)×10 [3] (3.18±0.05)×10 [29]

07.02.2023 N28E02 M3.8 22:58  - 22:53 22:55 23:03 10 61.0 13.3 65.4±1.9 (6.99±0.11)×10 [27]

07.02.2023 N30E03 M6.4 23:07 23:06 23:07 23:07 23:09 2.0 55.5 22.8 230±3.5 (2.53±0.04)×10 [28]

08.02.2023 N30E01 M2.1 02:53 02:53 02:53 02:53 02:53 <2.0 31.6 16.0 67.0±1.2 (5.06±0.08)×10 [27]

09.02.2023 S09E69 M1.1 07:17 07:17 07:17 07:17 07:19 2.0 23.2 15.0 273±21 (2.58±0.04)×10 [28]

10.02.2023 N30W23 M3.7 03:03  - 02:57 02:59 03:07 10 22.5 13.8 89.1±3.8 (6.26±0.10)×10 [27]

10.02.2023 N31W27 M1.4 08:05 08:05 08:05 08:05 08:07 2.0 26.0 14.8 82.7±3.7 (7.95±0.12)×10 [27]

11.02.2023 N07W69 M2.2 08:08 08:06 08:03 08:05 08:07 4.0 16.9 11.9 18.3±0.41 (3.07±0.05)×10 [27]

11.02.2023 S10E39 X1.1 15:48 15:46 15:41 15:47 16:01 20 51.8 23.9 841±15 (2.71±0.05)×10 [29]

12.02.2023 S10E29 M3.1 08:48 08:44 08:45 08:45 08:51 6.0 25.8 16.1 98.8±1.8 (1.36±0.02)×10 [28]

17.02.2023 N25E67 X2.3 20:16 20:02 19:58 20:02 20:42 44 61.6 24.4 (1.77±0.25)×10 [3] (1.45±0.02)×10 [30]

03.03.2023 N21W76 X2.1 17:52  - 17:50 17:50 18:06 16 203 62.1 (2.32±0.43)×10 [3] (5.83±0.10)×10 [29]

06.03.2023 N18W63 M5.8 02:28 02:21 02:20 02:22 02:32 12 32.3 13.1 222±41 (1.94±0.03)×10 [29]

29.03.2023 S21W59 X1.2 02:33  - 02:30 02:32 02:40 10 45.6 17.3 748±126 (3.36±0.05)×10 [29]

30.03.2023 S22W77 M5.4 07:37  - 07:33 07:35 07:37 4.0 25.9 16.6 (1.08±0.11)×10 [3] (1.02±0.05)×10 [29]

27.04.2023 S22E05 M1.8 11:14 11:12 11:13 11:13 11:19 6.0 29.5 17.4 74.4±0.81 (2.19±0.04)×10 [28]

03.05.2023 N13E43 M4.3 09:27  - 09:23 09:25 09:31 8.4 36.0 20.0 141±2.1 (2.03±0.04)×10 [28]

03.05.2023 N12E42 M3.1 10:14 10:12 10:09 10:11 10:11 1.7 16.5 12.6 32.4±0.30 (5.82±0.12)×10 [26]

03.05.2023 N12E42 M7.2 10:45 10:40 10:44 10:44 10:52 7.8 67.9 28.7 234±2.0 (6.25±0.12)×10 [28]

03.05.2023 N12E41 M1.7 12:35 12:34 12:30 12:35 12:44 15 30.2 21.9 76.3±0.64 (1.24±0.02)×10 [28]

03.05.2023 N12E40 M2.2 13:50 13:47 13:47 13:47 13:53 6.6 38.7 20.6 125±1.0 (2.55±0.05)×10 [28]

09.05.2023 N13W26 M6.5 03:54 03:51 03:47 03:53 04:11 24 35.9 20.0 111±6.1 (4.86±0.08)×10 [28]

18.05.2023 N17E77 M3.9 20:23 20:22 20:22 20:22 20:28 6.0 43.3 22.9 417±64 (1.53±0.03)×10 [29]

19.05.2023 N17E79 M5.4 00:48 00:44 00:44 00:44 00:50 6.0 32.7 22.1 298±45 (7.26±0.13)×10 [28]

20.05.2023 N17E55 M5.7 15:00 14:59 14:52 14:58 15:14 22 56.7 25.8 396±7.0 (1.33±0.03)×10 [29]


1The flare location is derived from the GOES flare catalog.
2The HXR peak means the peak time of the HXI 20 – 50 keV emission. Note that some WLFs have no available
data from HXI, which are tagged as “-”.
3There are three flares whose WL duration is less than two minutes. This is because their WL brightenings only
appear in one time frame.
4The uncertainty comes from the maximum difference between the WL brightening locations and the flare location
in the process of correcting project effect.
5The uncertainty of total flux consists of two parts, one from the average photometric fluctuation of 1.5% and
the other from the uncertainty of the radiometric calibration factor that is obtained via a comparison between
the observed counts of WST and standard irradiance at 360 nm from ASTM G173-03.


SOLA: paper.tex; 17 January 2024; 4:05; p. 16


A Statistical Study of WLFs Observed by WST
