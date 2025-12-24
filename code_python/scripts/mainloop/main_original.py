from rich.progress import Progress
from matplotlib.patches import Rectangle
from code_python.scripts.preprocessing.get_hdf5_data import *
from code_python.scripts.setup.calculation_setup import *
from code_python.scripts.config.parameters import *
# import code_python.scripts.mainloop.shock_speed_calculation as shock_speed_calculation

# with (Progress() as progress):
#     task = progress.add_task(f"[white] processing...", total=folder_count)
#     for COUNT, FILENAME in enumerate(folders):
#         data = read_timestep(filename=FILENAME)
#
#         current_timestep = data['t']
#
#         jx_e             = data['jx_e']
#         jy_e             = data['jy_e']
#         jz_e             = data['jz_e']
#         ke_e             = data['ke_e']
#         px_e             = data['px_e']
#         py_e             = data['py_e']
#         pz_e             = data['pz_e']
#         rho_e            = data['rho_e']
#         txx_e            = data['txx_e']
#         txy_e            = data['txy_e']
#         tyy_e            = data['tyy_e']
#         tyz_e            = data['tyz_e']
#         tzx_e            = data['tzx_e']
#         tzz_e            = data['tzz_e']
#
#         jx_i             = data['jx_i']
#         jy_i             = data['jy_i']
#         jz_i             = data['jz_i']
#         ke_i             = data['ke_i']
#         px_i             = data['px_i']
#         py_i             = data['py_i']
#         pz_i             = data['pz_i']
#         rho_i            = data['rho_i']
#         txx_i            = data['txx_i']
#         txy_i            = data['txy_i']
#         tyy_i            = data['tyy_i']
#         tyz_i            = data['tyz_i']
#         tzx_i            = data['tzx_i']
#         tzz_i            = data['tzz_i']
#
#         cex              = data['cex']
#         cey              = data['cey']
#         cez              = data['cez']
#         cbx              = data['cbx']
#         cby              = data['cby']
#         cbz              = data['cbz']
#
#
#         # ----------------------- CALCULATION PART ----------------------- #
#         if IS_CALCULATING_SHOCK_VELOCITY:
#             peak_value: float = shock_speed_calculation.get_shock_peak_index(rho_i)
#             x_peak: float = peak_value * dx_de  # [length unit]
#             t_peak: float = current_timestep * dt_wpe  # [time unit]
#             shock_speed_calculation.shock_distances.append(x_peak)
#             shock_speed_calculation.shock_times.append(t_peak)
#
#         if CHANGE_TO_DATA_IN_BOX_FRAME and V_SH > 0:
#             x_step = int(V_SH * (1 / dx_de) * dt_wpe * current_timestep)
#             box_index = [BOX_FRAME[0] + x_step, BOX_FRAME[0] + x_step + BOX_FRAME[2]]
#             # Ensure box is inside cell
#             if box_index[0] < X_SIZE[0] or box_index[1] > X_SIZE[1]:
#                 progress.update(task, advance=1)
#                 dump_process(f"Option CHANGE_TO_DATA_IN_BOX_FRAME is enabled. skipped T.{current_timestep}: box outside cell.")
#                 continue
#
#             jx_e = jx_e[box_index[0]: box_index[1], :]
#             jy_e = jy_e[box_index[0]: box_index[1], :]
#             jz_e = jz_e[box_index[0]: box_index[1], :]
#             ke_e = ke_e[box_index[0]: box_index[1], :]
#             px_e = px_e[box_index[0]: box_index[1], :]
#             py_e = py_e[box_index[0]: box_index[1], :]
#             pz_e = pz_e[box_index[0]: box_index[1], :]
#             rho_e = rho_e[box_index[0]: box_index[1], :]
#             txx_e = txx_e[box_index[0]: box_index[1], :]
#             txy_e = txy_e[box_index[0]: box_index[1], :]
#             tyy_e = tyy_e[box_index[0]: box_index[1], :]
#             tyz_e = tyz_e[box_index[0]: box_index[1], :]
#             tzx_e = tzx_e[box_index[0]: box_index[1], :]
#             tzz_e = tzz_e[box_index[0]: box_index[1], :]
#
#             jx_i = jx_i[box_index[0]: box_index[1], :]
#             jy_i = jy_i[box_index[0]: box_index[1], :]
#             jz_i = jz_i[box_index[0]: box_index[1], :]
#             ke_i = ke_i[box_index[0]: box_index[1], :]
#             px_i = px_i[box_index[0]: box_index[1], :]
#             py_i = py_i[box_index[0]: box_index[1], :]
#             pz_i = pz_i[box_index[0]: box_index[1], :]
#             rho_i = rho_i[box_index[0]: box_index[1], :]
#             txx_i = txx_i[box_index[0]: box_index[1], :]
#             txy_i = txy_i[box_index[0]: box_index[1], :]
#             tyy_i = tyy_i[box_index[0]: box_index[1], :]
#             tyz_i = tyz_i[box_index[0]: box_index[1], :]
#             tzx_i = tzx_i[box_index[0]: box_index[1], :]
#             tzz_i = tzz_i[box_index[0]: box_index[1], :]
#
#             cex = cex[box_index[0]: box_index[1], :]
#             cey = cey[box_index[0]: box_index[1], :]
#             cez = cez[box_index[0]: box_index[1], :]
#             cbx = cbx[box_index[0]: box_index[1], :]
#             cby = cby[box_index[0]: box_index[1], :]
#             cbz = cbz[box_index[0]: box_index[1], :]
#         if IS_CALCULATING_LORENTZ_TRANSFORMATION and V_SH > 0:
#             rho_i_prime = GAMMA * (rho_i - V_SH * jx_i)
#             jx_i_prime = GAMMA * (jx_i - rho_i * V_SH)
#             jy_i_prime = jy_i
#             jz_i_prime = jz_i
#
#             rho_e_prime = GAMMA * (rho_e - V_SH * jx_e)
#             jx_e_prime = GAMMA * (jx_e - rho_e * V_SH)
#             jy_e_prime = jy_e
#             jz_e_prime = jz_e
#
#             cex_prime = GAMMA * cex - GAMMA * GAMMA * V_SH / (GAMMA + 1) * (V_SH * cex)
#             cey_prime = GAMMA * (cey - V_SH * cbz)
#             cez_prime = GAMMA * (cez + V_SH * cby)
#
#             cbx_prime = GAMMA * cbx - GAMMA * GAMMA * V_SH / (GAMMA + 1) * (V_SH * cbx)
#             cby_prime = GAMMA * (cby + V_SH * cez)
#             cbz_prime = GAMMA * (cbz - V_SH * cey)
#         # TODO: Custom advanced function if there any derived calculation
#         if ENABLE_ADVANCED_CALCULATION:
#             ...
#             dump_process(f"[{COUNT+1}] Finish add sum T.{current_timestep}")
#         # ----------------------------------------------------------------- #
#
#
#     #     # ------------------------- PLOTTING PART ------------------------- #
#     #     if ENABLE_PLOT_FLOW_FIGURE:
#     #         for var, vbar, cmap in FLOW_LIST:
#     #             _: np.ndarray
#     #             exec(f'_ = {var}')
#     #             fig1.plot_figure(timestep=current_timestep, data=_, vbar=vbar, cmap=cmap, title=var)
#     #
#     #             if V_SH > 0:
#     #                 x_step = int(V_SH * (1 / dx_de) * dt_wpe * current_timestep)
#     #                 box_index = [BOX_FRAME[0] + x_step, BOX_FRAME[0] + x_step + BOX_FRAME[2]]
#     #                 update_x_limit = (BOX_FRAME[0] + x_step, BOX_FRAME[0] + BOX_FRAME[2] + x_step)
#     #
#     #                 if VISUAL_MOVING_BOX:
#     #                     fig1.ax.add_patch(
#     #                         Rectangle((BOX_FRAME[0] + x_step, BOX_FRAME[1]), BOX_FRAME[2], BOX_FRAME[3], linewidth=2,
#     #                                   edgecolor='black', facecolor='none'))
#     #
#     #                 if VISUAL_LINE:
#     #                     # Avoid the code plots mistake line at timestep T.0
#     #                     if current_timestep == 0:
#     #                         fig1.plot_line(update_x_limit[0] + (update_x_limit[1] - update_x_limit[0]) * LINE_RATIO_POSITION,
#     #                                        0)
#     #                     else:
#     #                         fig1.plot_line(update_x_limit[0] + (update_x_limit[1] - update_x_limit[0]) * LINE_RATIO_POSITION,
#     #                                        get_shock_peak_index(_))
#     #
#     #             save_figure(filename=f"{var}_T{current_timestep}")
#     #             fig1.clear()
#     #     if ENABLE_PLOT_ONE_GRAPH:
#     #         _: np.ndarray
#     #         auto_enable_legend: bool = False
#     #
#     #         if len(ONE_GRAPH_LIST) > 1 or ONE_GRAPH_TITLE != "":
#     #             title = ONE_GRAPH_TITLE
#     #         else:
#     #             title = ONE_GRAPH_LIST[0]
#     #
#     #         for i, var in enumerate(ONE_GRAPH_LIST):
#     #             exec(f"_ = {var}")
#     #
#     #             legend = var
#     #             if len(ONE_GRAPH_LIST) > 1:
#     #                 auto_enable_legend = True
#     #
#     #             fig2.plot(timestep=current_timestep, data=_, color=ONE_GRAPH_COLOR_LIST[i], label=legend, title=title)
#     #
#     #         if ONE_GRAPH_SET_Y_LIMIT != (0, 0):
#     #             fig2.ax.set_ylim(ONE_GRAPH_SET_Y_LIMIT)
#     #             fig2.ax.set_yticks(np.linspace(ONE_GRAPH_SET_Y_LIMIT[0], ONE_GRAPH_SET_Y_LIMIT[1], 5))
#     #
#     #         if auto_enable_legend:
#     #             fig2.ax.legend(loc='upper right')
#     #
#     #         if len(ONE_GRAPH_LIST) > 1 or ONE_GRAPH_FIGURE_FILENAME != "":
#     #             filename = ONE_GRAPH_FIGURE_FILENAME
#     #         else:
#     #             filename = ONE_GRAPH_LIST[0]
#     #
#     #         save_figure(filename=filename + str(current_timestep))
#     #         plt.cla()
#     #     # FIXME: Too lazy to improve performance
#     #     if ENABLE_PLOT_THREE_GRAPH or ENABLE_PLOT_SIX_GRAPH:
#     #         fig3 = PlotMultipleGraphFigure()
#     #         if TIME_UNIT_OPTION == 0:
#     #             fig3.fig.suptitle(f"{MULTIPLE_GRAPH_FIGURE_TITLE} at time {current_timestep} (code unit)")
#     #         elif TIME_UNIT_OPTION == 1:
#     #             fig3.fig.suptitle(f"{MULTIPLE_GRAPH_FIGURE_TITLE} at time {(current_timestep * dt_wpe):.04f}$\\omega_{{pe}}^{{-1}}$")
#     #         elif TIME_UNIT_OPTION == 2:
#     #             fig3.fig.suptitle(f"{MULTIPLE_GRAPH_FIGURE_TITLE} at time {(current_timestep * dt_wci):.04f}$\\Omega_{{ci}}^{{-1}}$")
#     #
#     #         for i, var_names in enumerate(MULTIPLE_GRAPH_LIST):
#     #             ax_index: int or tuple[int, int]
#     #             if i == 0:
#     #                 ax_index = [0, 0]
#     #             elif i == 1:
#     #                 ax_index = [1, 0]
#     #             elif i == 2:
#     #                 ax_index = [2, 0]
#     #             elif i == 3:
#     #                 ax_index = [0, 1]
#     #             elif i == 4:
#     #                 ax_index = [1, 1]
#     #             elif i == 5:
#     #                 ax_index = [2, 1]
#     #             else:
#     #                 raise IndexError
#     #             if ENABLE_PLOT_THREE_GRAPH and not ENABLE_PLOT_SIX_GRAPH:
#     #                 if len(MULTIPLE_GRAPH_LIST) > 3:
#     #                     raise IndexError("You have enabled 'ENABLE_PLOT_THREE_GRAPH', but your "
#     #                                      "'VARIABLE_MULTIPLE_GRAPH_LIST' exceeds more than 3. Or please enable "
#     #                                      "'ENABLE_PLOT_SIX_GRAPH = True.'")
#     #             data: np.ndarray
#     #             _label: str
#     #             for j, var_name in enumerate(var_names):
#     #                 exec(f"data = {var_name}")
#     #                 _label = ""
#     #                 try:
#     #                     if MULTIPLE_GRAPH_LEGEND_LIST[j] != "":
#     #                         _label = MULTIPLE_GRAPH_LEGEND_LIST[j]
#     #                 except IndexError: ...
#     #                 fig3.plot(ax_index=ax_index, data=data, color=MULTIPLE_GRAPH_COLOR_LIST[j], label=_label)
#     #                 if MULTIPLE_GRAPH_SET_Y_LIMITS[ax_index[0]][ax_index[1]] != (0, 0):
#     #                     fig3.axes[ax_index[0], ax_index[1]].set_ylim(MULTIPLE_GRAPH_SET_Y_LIMITS[ax_index[0]][ax_index[1]])
#     #         handles, labels = [], []
#     #         for line in fig3.axes[0, 0].get_lines():
#     #             handles.append(line)
#     #             labels.append(line.get_label())
#     #         fig3.fig.legend(handles, labels)
#     #         plt.tight_layout()
#     #         save_figure(filename=f"{MULTIPLE_GRAPH_FIGURE_FILENAME}_T{current_timestep}")
#     #         plt.close()
#     #
#     #     # Progress update when finish each timestep
#     #     progress.update(task, advance=1)
#     # plt.close()
# -------------------------------------------------------------------------------------------- #
# if IS_CALCULATING_SHOCK_VELOCITY:
#     calculate_shock_velocity()
#     save_figure(filename="Shock_velocity")
#     plt.close()
#
# if IS_EXPORT_DATA_TO_CSV:
#     ...
#
# dump_files(TIME_START)

# /pscratch/sd/k/kittiya/mean_project/vpic2/code_python2/csv_files/