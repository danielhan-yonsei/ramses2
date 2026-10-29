The namelist block `&RT_PARAMS` is used to specify parameters controlling the radiative transfer M1 solver and the coupling of the radiation with the gas.

| Variable name | Fortran type | Default value  | Description      |
|:------------------- |:-------|:----- |:------------------------- |
| `rt_advect`         | `logical`   | `.false.`  | Turn on and off radiation advection. It is off by default and turned on automatically once radiation sources appear for the first time in the simulation. |
| `rt_otsa`           | `logical`   | `.true.`   | Turn on and off the on the spot approximation for ionizing radiation. |
| `rt_smooth`         | `logical`   | `.true.`   | Turn on and off rt smoothing. This means we add the radiation fluxes progressively during the thermo-chemistry step. This is usually faster but not strictly conservative anymore. |
| `rt_c_fraction`     | `real`      | 1.0        | Fraction of the true speed of light used to define the adopted reduced speed of light. |
| `rt_nsubcycle`      | `integer`   | 1          | Maximum number of radiation substeps allowed per hydro steps. This is usually faster but not strictly conservative anymore in case of AMR. |
| `rt_isIR`           | `logical`   | `.false.`  | Treat photon group 1 as an infrared group: the radiation that dust absorbs in the other groups is re-emitted into it, and its photons scatter on dust (`kappaSc(1)`) and exchange energy with the gas through dust absorption and emission (`kappaAbs(1)`). |
| `is_kIR_T`          | `logical`   | `.false.`  | Scale the infrared opacities `kappaAbs(1)` and `kappaSc(1)` with the local radiation temperature `T_R` as `(T_R/10 K)^2 exp(-T_R/1000 K)`. `T_R` follows from the radiation energy density, the other groups weighted by their opacity relative to the infrared group. With more than one group, `kappaAbs(1)` must be positive. |
| `rt_T_rad`          | `logical`   | `.false.`  | Set the gas temperature to the radiation temperature `T_R` (plus the polytrope temperature, see `eos_T2`) instead of evolving it with heating, cooling and the infrared exchange. `T_R` is computed only with `is_kIR_T=.true.`; without it the temperature is left unchanged. |
| `rt_isoPress`       | `logical`   | `.false.`  | Compute the radiation force from the photon density (`cN` along the flux direction) instead of the photon flux `F`, as for a reduced flux of 1, for all groups but the infrared group of `rt_isIR`. |
| `rt_pressBoost`     | `real`      | 1.0        | Factor multiplying the momentum that the radiation gives to the gas. |
| `iPEH_group`        | `integer`   | -1         | Photon group used for photoelectric heating on dust; 0 or less turns it off. `kappaAbs` should not include the photoelectric absorption, which is added separately. Not used with `DO_RTZ`, whose cooling has its own photoelectric heating. |
