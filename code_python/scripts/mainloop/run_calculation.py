from rich.progress import Progress # Show run pregress
from code_python.scripts.config.parameters import *
from code_python.scripts.setup.calculation_setup import *
from code_python.scripts.preprocessing.get_hdf5_data import folders, folder_count, read_timestep
import code_python.scripts.dumping_backup_python_output as backup
import code_python.scripts.mainloop.shock_speed_calculation as shock_speed_calculation

DATE_START = backup.datetime.now()

with (Progress() as progress):
    task = progress.add_task(f"[white] processing...", total=folder_count)
    for folder_index, folder_name in enumerate(folders):
        data = read_timestep(shock_folder=folder_name)

        current_timestep = data['t']

        jx_e             = data['jx_e']
        jy_e             = data['jy_e']
        jz_e             = data['jz_e']
        ke_e             = data['ke_e']
        px_e             = data['px_e']
        py_e             = data['py_e']
        pz_e             = data['pz_e']
        rho_e            = data['rho_e']
        txx_e            = data['txx_e']
        txy_e            = data['txy_e']
        tyy_e            = data['tyy_e']
        tyz_e            = data['tyz_e']
        tzx_e            = data['tzx_e']
        tzz_e            = data['tzz_e']

        jx_i             = data['jx_i']
        jy_i             = data['jy_i']
        jz_i             = data['jz_i']
        ke_i             = data['ke_i']
        px_i             = data['px_i']
        py_i             = data['py_i']
        pz_i             = data['pz_i']
        rho_i            = data['rho_i']
        txx_i            = data['txx_i']
        txy_i            = data['txy_i']
        tyy_i            = data['tyy_i']
        tyz_i            = data['tyz_i']
        tzx_i            = data['tzx_i']
        tzz_i            = data['tzz_i']

        cex              = data['cex']
        cey              = data['cey']
        cez              = data['cez']
        cbx              = data['cbx']
        cby              = data['cby']
        cbz              = data['cbz']

        # ----------------------- CALCULATION PART ----------------------- #
        # Calculating shock speed by tracking time evolution of peak charge density location
        if IS_CALCULATING_SHOCK_SPEED:
            peak_value: float = shock_speed_calculation.get_shock_peak_index(rho_i)
            x_peak: float = peak_value * dx_de  # [length unit]
            t_peak: float = current_timestep * dt_wpe  # [time unit]
            shock_speed_calculation.shock_distances.append(x_peak)
            shock_speed_calculation.shock_times.append(t_peak)

        # Change data to box frame (Lorentz transformation frame)
        if IS_CALCULATING_LORENTZ_TRANSFORMATION:
            # Use gamma = 1 / sqrt(1 - v^2), where c = 1 (normalized units)
            GAMMA = (1 - target_velocity ** 2) ** (-1 / 2)
            x_step = int(V_SH * (1 / dx_de) * dt_wpe * current_timestep)
            box_index = [box_frame[0] + x_step, box_frame[0] + x_step + box_frame[2]]
            # Ensure box frame insides simulation frame
            if box_index[0] < 0 or box_index[1] > nx:
                progress.update(task, advance=1)
                backup.dump_process(f"Not calculated Lorentz transformation at T.{current_timestep}: box frame outsides simulation frame.")
                continue

            jx_e = jx_e[box_index[0]: box_index[1], :]
            jy_e = jy_e[box_index[0]: box_index[1], :]
            jz_e = jz_e[box_index[0]: box_index[1], :]
            ke_e = ke_e[box_index[0]: box_index[1], :]
            px_e = px_e[box_index[0]: box_index[1], :]
            py_e = py_e[box_index[0]: box_index[1], :]
            pz_e = pz_e[box_index[0]: box_index[1], :]
            rho_e = rho_e[box_index[0]: box_index[1], :]
            txx_e = txx_e[box_index[0]: box_index[1], :]
            txy_e = txy_e[box_index[0]: box_index[1], :]
            tyy_e = tyy_e[box_index[0]: box_index[1], :]
            tyz_e = tyz_e[box_index[0]: box_index[1], :]
            tzx_e = tzx_e[box_index[0]: box_index[1], :]
            tzz_e = tzz_e[box_index[0]: box_index[1], :]

            jx_i = jx_i[box_index[0]: box_index[1], :]
            jy_i = jy_i[box_index[0]: box_index[1], :]
            jz_i = jz_i[box_index[0]: box_index[1], :]
            ke_i = ke_i[box_index[0]: box_index[1], :]
            px_i = px_i[box_index[0]: box_index[1], :]
            py_i = py_i[box_index[0]: box_index[1], :]
            pz_i = pz_i[box_index[0]: box_index[1], :]
            rho_i = rho_i[box_index[0]: box_index[1], :]
            txx_i = txx_i[box_index[0]: box_index[1], :]
            txy_i = txy_i[box_index[0]: box_index[1], :]
            tyy_i = tyy_i[box_index[0]: box_index[1], :]
            tyz_i = tyz_i[box_index[0]: box_index[1], :]
            tzx_i = tzx_i[box_index[0]: box_index[1], :]
            tzz_i = tzz_i[box_index[0]: box_index[1], :]

            cex = cex[box_index[0]: box_index[1], :]
            cey = cey[box_index[0]: box_index[1], :]
            cez = cez[box_index[0]: box_index[1], :]
            cbx = cbx[box_index[0]: box_index[1], :]
            cby = cby[box_index[0]: box_index[1], :]
            cbz = cbz[box_index[0]: box_index[1], :]

            # Calculate Lorentz transformation (+x direction)
            rho_i_prime = GAMMA * (rho_i - V_SH * jx_i)
            jx_i_prime = GAMMA * (jx_i - rho_i * V_SH)
            jy_i_prime = jy_i
            jz_i_prime = jz_i

            rho_e_prime = GAMMA * (rho_e - V_SH * jx_e)
            jx_e_prime = GAMMA * (jx_e - rho_e * V_SH)
            jy_e_prime = jy_e
            jz_e_prime = jz_e

            cex_prime = GAMMA * cex - GAMMA * GAMMA * V_SH / (GAMMA + 1) * (V_SH * cex)
            cey_prime = GAMMA * (cey - V_SH * cbz)
            cez_prime = GAMMA * (cez + V_SH * cby)

            cbx_prime = GAMMA * cbx - GAMMA * GAMMA * V_SH / (GAMMA + 1) * (V_SH * cbx)
            cby_prime = GAMMA * (cby + V_SH * cez)
            cbz_prime = GAMMA * (cbz - V_SH * cey)

        # TODO: Custom advanced function if there any derived calculation
        if ENABLE_ADVANCED_CALCULATION:
            ...
            backup.dump_process(f"[{folder_index+1}] Finish add sum T.{current_timestep}")
        # ----------------------------------------------------------------- #

if IS_CALCULATING_SHOCK_SPEED:
    shock_speed_calculation.show_graph_of_shock_speed_tracking()

if IS_EXPORT_DATA_TO_CSV:
    ...

backup.save(DATE_START, output_path="calculation_path")

# test adding new text