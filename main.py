import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import messagebox
import time
from matplotlib.animation import *
import threading
matplotlib.use("TkAgg")



VP = 900
stop = False

trg_remaining_distance_list = []
target_distance_list = []
qpn_list = []
y1_value = []
y2_value = []
qp_list = []
wh_list = []
step_x_list = []
step_y_list = []


def ek_formula():

    H = int(target_height_input.get())
    D = int(target_distance_input.get())
    E0 = int(E0_input.get())
    T = int(T_input.get())

    for i in range(0, len(target_distance_list)):
        E_trg = np.arctan(H/D)
        Ek = E_trg + E0 * (np.e**(-i/T))
        Ek_result.config(text=("%.2f" % Ek))
        time.sleep(0.5)
    return


def wh_formula():

    global VP
    H = int(target_height_input.get())
    D = int(target_distance_input.get())
    t = 1
    S_trg = int(np.sqrt((D ** 2) - (H ** 2)))
    V = int(target_speed_input.get())
    trg_m_in_1_sec = V * t

    def plot1_trg_thread():

        for i in range(-1, S_trg):
            i += 1
            trg_remaining_distance = (S_trg - i * trg_m_in_1_sec)

            if trg_remaining_distance >= S_trg/3:
                x_value = np.arange(trg_remaining_distance, S_trg)
                y1_value.clear()

                for i in range(len(x_value)):
                    y1_value.append(H)

                a.plot(x_value, y1_value, color="green", label="Цель")
                canvas1.draw()
                canvas1.flush_events()
                time.sleep(0.5)

            elif trg_remaining_distance < S_trg/3:
                break
        return

    def plot1_missile_thread():

        for i in range(-1, S_trg):
            i += 1
            trg_remaining_distance = (S_trg - i * trg_m_in_1_sec)
            trg_remaining_distance_list.append(trg_remaining_distance)

            if trg_remaining_distance >= S_trg/3:
                new_target_distance = np.sqrt((H ** 2) + (trg_remaining_distance ** 2))
                target_distance_list.append(new_target_distance)
                y2_value.clear()

                for i in range(len(target_distance_list)):
                    y2_value.append(H)

                Qpn = (H / new_target_distance)
                qpn_list.append(Qpn)

            elif trg_remaining_distance < S_trg/3:
                break

        for i in range(0, len(qpn_list) - 1):
            if i <= len(qpn_list):
                Qp = (abs((qpn_list[i] - qpn_list[(i + 1)]) / t))
                qp_list.append(Qp)
            elif i > len(qpn_list):
                break

        for i in range(0, len(qp_list)):
            Wh = VP * qp_list[i]
            wh_list.append(Wh)
        return

    def plot1_missile_thread1():

        global stop
        stop = True

        for i in range(0, len(target_distance_list)):
            x = [0, trg_remaining_distance_list[i]]
            y = [0, H]

            if i == 0:
                step_x = [0, 0]
                step_y = [0, 0]
                step_x_list.append(step_x)
                step_y_list.append(step_y)

            elif i != 0:
                step_x = [trg_remaining_distance_list[i] / len(target_distance_list) * (i+1),
                          trg_remaining_distance_list[i] / len(target_distance_list) * (i+1)]
                step_y = [H / len(target_distance_list) * (i+1), H / len(target_distance_list) * (i+1)]

                step_x_list.append(step_x)
                step_y_list.append(step_y)

            try:
                Wh_result.config(text=("%.2f" % wh_list[i]))
            except:
                pass

            a.plot(x, y, color="black", linewidth=0.1, ls="--", label="Дистанция до цели")
            a.scatter(step_x_list[i], step_y_list[i], color="red", label="Ракета", s=5)

            if i == 0:
                a.legend()
            else:
                pass

            canvas1.draw()
            canvas1.flush_events()
            time.sleep(0.5)

        stop = False
        return stop

    thread1 = threading.Thread(target=plot1_trg_thread, daemon=True)
    thread2 = threading.Thread(target=plot1_missile_thread, daemon=True)
    thread3 = threading.Thread(target=plot1_missile_thread1, daemon=True)
    thread4 = threading.Thread(target=ek_formula, daemon=True)
    thread5 = threading.Thread(target=plot2_thread, daemon=True)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    return


def plot2_thread():

    for i in range(0, len(wh_list)):
        try:
            plot2_x = [target_distance_list[i], target_distance_list[i+1]]
            plot2_y = [wh_list[i], wh_list[i+1]]

            b.plot(plot2_x, plot2_y, color="blue", linewidth=0.7)
            canvas2.draw()
            canvas2.flush_events()
            time.sleep(0.5)
        except IndexError:
            pass
    return


def submit():
    try:
        wh_formula()
    except ValueError:
        messagebox.showerror("Ошибка", "Вы ввели некорректные значения.\n"
                                       "Ошибка также могла возникнуть в случае, если\n"
                                       "в заданных условиях ракета не способна попасть в цель.")


def clear():

    global stop

    if stop:
        messagebox.showinfo("Ожидание", "Дождитесь окончания расчетов")
    else:
        a.cla()
        a.grid()
        a.set_xlabel("Расстояние, м")
        a.set_ylabel("Высота, м")
        a.set_title("Траектория полёта ракеты")
        plot_figure1.tight_layout()
        canvas1.draw()

        b.cla()
        b.grid()
        b.set_xlabel("Дальность до цели (D)")
        b.set_ylabel("Норм. ускор. (Wн)")
        b.set_title("Зависимость нормального ускорения ракеты от дистанции до цели")
        plot_figure2.tight_layout()
        canvas2.draw()

        target_height_input.delete(0, 'end')
        target_distance_input.delete(0, 'end')
        E0_input.delete(0, 'end')
        T_input.delete(0, 'end')
        target_speed_input.delete(0, 'end')

        trg_remaining_distance_list.clear()
        target_distance_list.clear()
        qpn_list.clear()
        y1_value.clear()
        y2_value.clear()
        qp_list.clear()
        wh_list.clear()
        step_x_list.clear()
        step_y_list.clear()

        Wh_result.config(text="")
        Ek_result.config(text="")


window = Tk()

window.geometry("1160x510")
window.resizable(width=False, height=False)
window.title("Калькулятор трёхточечного метода наведения ракеты")

target_frame = Frame(window, height=500, width=300)
target_frame.grid(row=0, column=0, padx=10, pady=10)

HDV_frame = Frame(target_frame, borderwidth=1, relief="solid")
HDV_frame.pack(ipadx=40, ipady=20)

target_data_title = Label(HDV_frame, text="Исходные данные цели", font=("Arial", 15))
target_data_title.pack(padx=30, pady=5)

target_height = Label(HDV_frame, text="Высота цели (H), м: ", font=("Arial", 13))
target_height.pack(padx=5, pady=5)

target_height_input = Entry(HDV_frame, width=10)
target_height_input.pack(padx=5, pady=2)

target_distance = Label(HDV_frame, text="Дальность до цели (D), м: ", font=("Arial", 13))
target_distance.pack(padx=5, pady=5)

target_distance_input = Entry(HDV_frame, width=10)
target_distance_input.pack(padx=5, pady=2)

target_speed = Label(HDV_frame, text="Скорость цели (V), м/с: ", font=("Arial", 13))
target_speed.pack(padx=5, pady=5)

target_speed_input = Entry(HDV_frame, width=10)
target_speed_input.pack(padx=5, pady=2)

#---------------------------------------------------------------------------------------------

empty_frame = Frame(target_frame, height=30)
empty_frame.pack()

E0T_frame = Frame(target_frame)
E0T_frame.pack()

E0_label = Label(E0T_frame, text="E0: ", font=("Arial", 13))
E0_label.grid(row=0, column=0, padx=5, pady=5)

E0_input = Entry(E0T_frame, width=10)
E0_input.grid(row=0, column=1, pady=5)

T_label = Label(E0T_frame, text="T: ", font=("Arial", 13))
T_label.grid(row=0, column=3, pady=5)

T_input = Entry(E0T_frame, width=10)
T_input.grid(row=0, column=4, padx=5, pady=5)

Wh_label = Label(E0T_frame, text="Wн: ", font=("Arial", 13))
Wh_label.grid(row=2, column=1, padx=5, pady=5)

Wh_result = Label(E0T_frame,
                  width=15,
                  borderwidth=1,
                  relief="groove",
                  background="#e6e6e6",
                  text="",
                  font=("Arial", 10, "bold"))
Wh_result.grid(row=2, column=2, padx=5, pady=5)

Ek_label = Label(E0T_frame, text="Eк: ", font=("Arial", 13))
Ek_label.grid(row=3, column=1, padx=5, pady=5)

Ek_result = Label(E0T_frame,
                  width=15,
                  borderwidth=1,
                  relief="groove",
                  background="#e6e6e6",
                  text="",
                  font=("Arial", 10, "bold"))
Ek_result.grid(row=3, column=2, padx=5)

submit_btn = Button(E0T_frame, text="Построить", font=("Arial", 10, "bold"), command=submit)
submit_btn.grid(row=4, column=2, padx=5, pady=5)

clear_btn = Button(E0T_frame, text="Очистить", font=("Arial", 10, "bold"), command=clear)
clear_btn.grid(row=5, column=2, padx=5, pady=5)

#-----------------------------------------------------------------------------------------------------

empty_frame1 = Frame(window, width=20)
empty_frame1.grid(row=0, column=1)

plots_frame = Frame(window)
plots_frame.grid(row=0, column=2, sticky=N)

plot1_frame = Frame(plots_frame, borderwidth=1, relief="solid")
plot1_frame.grid(row=0, column=0)

plot_figure1 = Figure(figsize=(7.3, 3), dpi=100)
a = plot_figure1.add_subplot(111)
a.plot()
a.grid()
a.set_xlabel("Расстояние, м")
a.set_ylabel("Высота, м")
a.set_title("Траектория полёта ракеты")
plot_figure1.tight_layout()
canvas1 = FigureCanvasTkAgg(plot_figure1, plot1_frame)
canvas1.draw()
canvas1.get_tk_widget().pack()

plot2_frame = Frame(plots_frame, borderwidth=1, relief="solid")
plot2_frame.grid(row=1, column=0, sticky=N, pady=15)

plot_figure2 = Figure(figsize=(9.1, 2), dpi=80)
b = plot_figure2.add_subplot(111)
b.plot()
b.grid()
b.set_xlabel("Дальность до цели (D)")
b.set_ylabel("Норм. ускор. (Wн)")
b.set_title("Зависимость нормального ускорения ракеты от дистанции до цели")
plot_figure2.tight_layout()
canvas2 = FigureCanvasTkAgg(plot_figure2, plot2_frame)
canvas2.draw()
canvas2.get_tk_widget().pack()

window.mainloop()
