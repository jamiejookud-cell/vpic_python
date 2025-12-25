from rich.progress import Progress # Show run pregress
from code_python.scripts.config.parameters import *
from code_python.scripts.setup.calculation_setup import *
from code_python.scripts.setup.plotting_setup import *
from code_python.scripts.preprocessing.get_hdf5_data import folders, folder_count, read_timestep
from code_python.scripts.preprocessing.plotting_functions import PlotFlowFigure
import code_python.scripts.preprocessing.shock_speed_calculation as shock_speed_calculation
from code_python.scripts.preprocessing.custom_advanced_functions import *
import code_python.scripts.dumping_backup_python_output as backup

DATE_START = backup.datetime.now()

backup.dump_process("▀▄▀▄▀▄ MAINLOOP ▀▄▀▄▀▄")
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
        if not IS_CALCULATING_LORENTZ_TRANSFORMATION:
            backup.dump_process("(Disabled 'IS_CALCULATING_LORENTZ_TRANSFORMATION')")
        else:
            x0, length = box_frame[0], box_frame[2]
            v = target_velocity
            # Use gamma = 1 / sqrt(1 - v^2), where c = 1 (normalized units)
            gamma = (1 - v ** 2) ** (-1 / 2)
            x_step = int(v * (1 / dx_de) * dt_wpe * current_timestep)
            box_index = [x0 + x_step, (x0 + x_step) + length]
            # Ensure box frame insides simulation frame
            if box_index[0] < 0 or box_index[1] > nx:
                progress.update(task, advance=1)
                backup.dump_process(f"Not calculated Lorentz transformation at T.{current_timestep}: box frame outsides simulation frame.")
                continue

            _jx_e = jx_e[box_index[0]: box_index[1], :]
            _jy_e = jy_e[box_index[0]: box_index[1], :]
            _jz_e = jz_e[box_index[0]: box_index[1], :]
            _ke_e = ke_e[box_index[0]: box_index[1], :]
            _px_e = px_e[box_index[0]: box_index[1], :]
            _py_e = py_e[box_index[0]: box_index[1], :]
            _pz_e = pz_e[box_index[0]: box_index[1], :]
            _rho_e = rho_e[box_index[0]: box_index[1], :]
            _txx_e = txx_e[box_index[0]: box_index[1], :]
            _txy_e = txy_e[box_index[0]: box_index[1], :]
            _tyy_e = tyy_e[box_index[0]: box_index[1], :]
            _tyz_e = tyz_e[box_index[0]: box_index[1], :]
            _tzx_e = tzx_e[box_index[0]: box_index[1], :]
            _tzz_e = tzz_e[box_index[0]: box_index[1], :]

            _jx_i = jx_i[box_index[0]: box_index[1], :]
            _jy_i = jy_i[box_index[0]: box_index[1], :]
            _jz_i = jz_i[box_index[0]: box_index[1], :]
            _ke_i = ke_i[box_index[0]: box_index[1], :]
            _px_i = px_i[box_index[0]: box_index[1], :]
            _py_i = py_i[box_index[0]: box_index[1], :]
            _pz_i = pz_i[box_index[0]: box_index[1], :]
            _rho_i = rho_i[box_index[0]: box_index[1], :]
            _txx_i = txx_i[box_index[0]: box_index[1], :]
            _txy_i = txy_i[box_index[0]: box_index[1], :]
            _tyy_i = tyy_i[box_index[0]: box_index[1], :]
            _tyz_i = tyz_i[box_index[0]: box_index[1], :]
            _tzx_i = tzx_i[box_index[0]: box_index[1], :]
            _tzz_i = tzz_i[box_index[0]: box_index[1], :]

            _cex = cex[box_index[0]: box_index[1], :]
            _cey = cey[box_index[0]: box_index[1], :]
            _cez = cez[box_index[0]: box_index[1], :]
            _cbx = cbx[box_index[0]: box_index[1], :]
            _cby = cby[box_index[0]: box_index[1], :]
            _cbz = cbz[box_index[0]: box_index[1], :]

            # Calculate Lorentz transformation (+x direction)
            rho_i_prime = gamma * (_rho_i - v * _jx_i)
            jx_i_prime = gamma * (_jx_i - _rho_i * v)
            jy_i_prime = _jy_i
            jz_i_prime = _jz_i

            rho_e_prime = gamma * (_rho_e - v * _jx_e)
            jx_e_prime = gamma * (_jx_e - _rho_e * v)
            jy_e_prime = _jy_e
            jz_e_prime = _jz_e

            cex_prime = gamma * _cex - gamma * gamma * v / (gamma + 1) * (v * _cex)
            cey_prime = gamma * (_cey - v * _cbz)
            cez_prime = gamma * (_cez + v * _cby)

            cbx_prime = gamma * _cbx - gamma * gamma * v / (gamma + 1) * (v * _cbx)
            cby_prime = gamma * (_cby + v * _cez)
            cbz_prime = gamma * (_cbz - v * _cey)

        if not ENABLE_ADVANCED_CALCULATION:
            backup.dump_process("(Disabled 'ENABLE_ADVANCED_CALCULATION')")
        else:
            # TODO: doing derived calculation
            ...
            backup.dump_process(f"[{folder_index+1}] Finish calculation T.{current_timestep}")
        # ----------------------------------------------------------------- #

        # ------------------------- PLOTTING PART -------------------------
        """
        Enable built-in features:
        - PlotFlowFigure(timestep, data, vbar, cmap, units)
        available unit: de, di, wpe, wci
        prompt example: units = "de wpe" or "wpe de"

        Example usage:
            fig = PlotFlowFigure(current_timestep, data=rho_i, vbar=(0, 6), cmap=wtdr, units="di wci")
            fig.show_lorentz_frame() # show outline of box frame
            fig.save(filename="rho_i") # or fig.show()
        
        """
        fig1 = PlotFlowFigure(current_timestep, data=rho_i, vbar=(0, 6), cmap=wtdr, units="di wci")
        fig1.show_lorentz_frame(line_reference_ratio=0.5)
        fig1.draw_line_peak_position()
        fig1.save("rho_i")

        # ----------------------------------------------------------------- #
backup.dump_process("▀▄▀▄▀▄ ENDLOOP ▀▄▀▄▀▄")

if IS_CALCULATING_SHOCK_SPEED:
    shock_speed_calculation.show_graph_of_shock_speed_tracking()

if not IS_EXPORT_DATA_TO_CSV:
    backup.dump_process("(Disabled 'IS_EXPORT_DATA_TO_CSV')")
else:
    # TODO: For export data
    ...

backup.save(DATE_START)