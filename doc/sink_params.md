The three namelist blocks `&SINK_PARAMS`, `&SINK_ACCRETION_PARAMS` and `&SINK_FEEDBACK_PARAMS` control the sink particle module. Sinks are used to model gravitationally-collapsing structures such as forming stars or accreting black holes. Sink formation reuses the PHEW clump finder to detect formation sites; accretion follows a Bondi-Hoyle-Lyttleton or flux-based scheme; feedback follows a two-mode (quasar/radio) AGN model.

## `&SINK_PARAMS`: formation and dynamics

| Variable name              | Fortran type | Default value | Description                                                                                        |
|:---------------------------|:-------------|:--------------|:---------------------------------------------------------------------------------------------------|
| `sink`                     | `logical`    | `.false.`     | Turn the sink particle module on or off.                                                           |
| `nsinkmax`                 | `integer`    | 0             | Maximum number of sink particles that can be allocated per MPI process.                            |
| `nsinktot`                 | `integer(8)` | 0             | Total maximum number of sink particles across all MPI processes.                                   |
| `rho_type_sink`            | `integer`    | 1             | Fluid used to build the density field for sink formation (1: DM, 2: stars, 3: sinks, 4: gas).      |
| `sink_form`                | `logical`    | `.false.`     | Activate sink particle formation.                                                                  |
| `nstep_per_sink`           | `integer`    | 1             | Call sink formation every `nstep_per_sink` coarse steps.                                          |
| `sink_merge`               | `logical`    | `.false.`     | Activate sink-sink merging.                                                                        |
| `sink_dump`                | `logical`    | `.false.`     | Dump sink particle data on the fly (in `dump/`).                                                   |
| `sink_delta_tout`          | `real`       | 0             | Time interval (in Myr) between successive high-frequency sink dumps in `sinklog/`.                         |
| `sink_recenter_on_peak`    | `logical`    | `.true.`      | Reset the position of newly formed sinks to the centre of mass of their host peak.                 |
| `sink_descent`             | `logical`    | `.false.`     | Activate the density-gradient descent to relocate sinks onto local peaks.                          |
| `fudge_descent`            | `real`       | 0.5           | Step size used by the density-gradient descent.                                                    |
| `sink_relevance_threshold` | `real`       | 2             | Peak relevance threshold used for sink formation sites.                                            |
| `sink_density_threshold`   | `real`       | -1            | Density threshold (code units) above which peaks are considered for sink formation. Must be > 0 when `sink_form` is set. |
| `sink_saddle_threshold`    | `real`       | -1            | Saddle-point density threshold for merging peaks into halo-patches for sinks.                      |
| `sink_mass_threshold`      | `real`       | 0             | Minimum clump mass (code units) required to form a sink.                                           |
| `sink_purity_threshold`    | `real`       | -1            | Minimum high-resolution mass fraction (for zoom simulations).                                      |
| `sink_fraction_threshold`  | `real`       | 2             | Sub-halo mass fraction threshold used to identify main halos as formation sites.                   |
| `sink_mseed`               | `real`       | 1e6           | Seed mass of newly formed sinks in solar masses.                                                               |
| `sink_nstar_frac`          | `real`       | -1            | Gas density threshold for sink formation in units of the star-formation density `n_star`.                      |
| `drag_sink`                | `logical`    | `.false.`     | Enable gaseous dynamical friction (Ostriker 1999) on sink particles.                               |
| `verbose_sink`             | `logical`    | `.false.`     | Print verbose diagnostics for sink particles.                                                      |

## `&SINK_ACCRETION_PARAMS`: accretion

| Variable name           | Fortran type | Default value | Description                                                                                                    |
|:------------------------|:-------------|:--------------|:---------------------------------------------------------------------------------------------------------------|
| `accretion_type`        | `integer`    | 0             | Accretion recipe: 0 = none, 1 = Bondi-Hoyle-Lyttleton, 2 = flux (Bleuler+14), 3 = density threshold. |
| `acc_sink_boost`        | `real`       | 1             | Boost factor for the Bondi accretion rate.                                                                     |
| `bondi_use_vrel`        | `logical`    | `.true.`      | Include the relative sink-gas velocity in the Bondi denominator.                                               |
| `bondi_use_gas_mass`    | `logical`    | `.false.`     | Add the local gas mass to the sink mass when computing the Bondi radius.                                       |
| `use_local_bondi_rate`  | `logical`    | `.false.`     | Compute the Bondi rate per cell and weight-average, rather than averaging gas properties first.                |
| `use_rho_inf`           | `logical`    | `.true.`      | Extrapolate the density at infinity using the Krumholz et al. (2004) `bondi_alpha` function.                   |
| `use_bondi_lambda`      | `logical`    | `.true.`      | Use the transonic Bondi eigenvalue `lambda_sonic(gamma)` in the accretion rate.                                |
| `eddington_cap`         | `real`       | -1            | Cap accretion at this multiple of the Eddington rate (disabled if negative).                                   |
| `eddington_floor`       | `real`       | -1            | Skip accretion when the rate falls below this fraction of Eddington (disabled if negative).                    |
| `manual_accretion_rate` | `real`       | -1            | If positive, force the accretion rate to this fraction of Eddington (overrides the Bondi/flux calculation).    |
| `sink_b_spline_order`   | `integer`    | 4             | Order of the B-spline kernel used to gather gas properties around a sink (2 = CIC, 3 = TSC, 4 = PCS).          |
| `mass_weighting`        | `logical`    | `.true.`      | Weight the per-cell accretion by the local density (rather than by kernel weight only).                        |
| `momentum_conserving`   | `logical`    | `.false.`     | Transfer the accreted momentum, position offset and angular momentum to the sink.                              |
| `sink_fix_mass`         | `logical`    | `.false.`     | Freeze the sink mass (still remove accreted mass from the gas).                                                |
| `static_sink`           | `logical`    | `.false.`     | Freeze the sink position (velocity and momentum are still updated).                                            |
| `t_start_black_hole`    | `real`       | -1            | Delay time (code units, since sink birth) before accretion/feedback fully turn on. Ramp-up is exponential.     |
| `sink_mechanical`       | `logical`    | `.false.`     | Use the 56-point multi-level stencil (as in mechanical SN feedback) for accretion, drag and AGN feedback, so `sink_refine` is not needed. Supports `accretion_type` 0, 1 or 3 only; ignores `sink_b_spline_order`, `agn_feedback_radius` and `agn_jet_opening_angle` (cylindrical jet over the whole stencil). |

## `&SINK_FEEDBACK_PARAMS`: AGN feedback

| Variable name                   | Fortran type | Default value | Description                                                                                        |
|:--------------------------------|:-------------|:--------------|:---------------------------------------------------------------------------------------------------|
| `agn`                           | `logical`    | `.false.`     | Activate AGN feedback around sink particles.                                                       |
| `agn_feedback_radius`           | `integer`    | 4             | Radius of the feedback region in units of the finest cell size (should be >= `sink_b_spline_order/2`). |
| `agn_weighting_scheme`          | `integer`    | 1             | Weighting scheme used by the `psy_function` to distribute feedback across the region.              |
| `agn_fbk_mode_switch_threshold` | `real`       | 0.01          | Eddington ratio below which the code switches from quasar (thermal) to radio (kinetic) mode.       |
| `epsilon_rad`                   | `real`       | 0.1           | Radiative efficiency `L = epsilon_rad * dM/dt * c^2`.                                              |
| `epsilon_quasar`                | `real`       | 0.15          | Coupling efficiency of the quasar-mode thermal energy injection.                                   |
| `epsilon_radio`                 | `real`       | 1             | Momentum of the radio-mode jet in units of `L/c`.                                                  |
| `agn_jet_opening_angle`         | `real`       | 60            | Full opening angle (degrees) of the radio-mode bipolar outflow cone.                               |
| `agn_use_mass_weighting`        | `logical`    | `.false.`     | Weight the feedback injection by the local gas density.                                            |
| `agn_jet_vmax`                  | `real`       | 1e4           | Maximum velocity kick (radio mode) and sound speed (quasar mode), in km/s, of the mass-loaded AGN feedback (`sink_mechanical` only). Must satisfy 0 < `agn_jet_vmax` <= c. |

With `sink_mechanical=.true.`, feedback is spread over the 56-point stencil
around the host cell. In radio mode all 56 points receive the jet, with the
velocity along the spin axis, upward or downward depending on their side of the
equatorial plane through the host cell centre (cylindrical jet, no opening angle).
In both modes, a fraction eta/(1+eta) of the accreted mass is not accreted but put
back into the gas with the feedback, and the luminosity L comes from the mass reaching
the black hole. The loading is the smallest one that keeps the radio-mode velocity kick
or the quasar-mode sound speed below `agn_jet_vmax`:
eta = max(0, (lambda*M_in - M_a)/(M_a + M_in)), with M_in the accreted mass, M_a the
ambient mass seen by the feedback (minimum over the sample points of the gas mass
divided by the fraction of the feedback it receives), and
lambda = `epsilon_radio*epsilon_rad*c/agn_jet_vmax` (radio) or
lambda = `gamma*(gamma-1)*epsilon_quasar*epsilon_rad*(c/agn_jet_vmax)**2` (quasar).
In quasar mode the cap is on the sound speed after heating: the ambient mass of each
sample point is reduced by the factor (1 - e/e_max), with e its specific thermal energy
and e_max = agn_jet_vmax**2/(gamma*(gamma-1)), and M_a is floored at 0, so that gas
already hotter than the cap does not get hotter.
There is no loading in dense gas. The energy added to each sample point is the change of
kinetic energy of its gas, plus the quasar-mode heating, so that its thermal energy
stays positive.
