import tkinter as tk
import pymysql
import datetime as dt
from time import gmtime, strftime

class task_scheduler(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Task scheduler')
        self.db = pymysql.Connect(host='localhost', port=3306, database='task_scheduler', user='root', password='123456',
                             charset='utf8')
        self.cursor = self.db.cursor()

        # generate unfinished task list
        self.frame1 = tk.Frame()
        self.label_list0 = tk.Label(self.frame1, text="Unfinished task list: ")
        self.label_list0.pack()
        self.scroll_bary0 = tk.Scrollbar(self.frame1)
        self.scroll_barx0 = tk.Scrollbar(self.frame1, orient=tk.HORIZONTAL)
        self.unfinished_task_list = tk.Listbox(self.frame1, width=100, height=20, xscrollcommand=self.scroll_barx0.set, yscrollcommand=self.scroll_bary0.set)
        self.generate_list(finished=False)
        self.scroll_bary0.pack(side="right", fill="y")
        self.scroll_barx0.pack(side="bottom", fill="x")
        self.unfinished_task_list.pack(side="left", fill="both")
        self.scroll_bary0.config(command = self.unfinished_task_list.yview)
        self.scroll_barx0.config(command = self.unfinished_task_list.xview)

        # generate finished task list
        self.frame4 = tk.Frame()
        self.label_list1 = tk.Label(self.frame4, text="Finished task list: ")
        self.label_list1.pack()
        self.scroll_bary1 = tk.Scrollbar(self.frame4)
        self.scroll_barx1 = tk.Scrollbar(self.frame4, orient=tk.HORIZONTAL)
        self.finished_task_list = tk.Listbox(self.frame4, width=100, height=10, xscrollcommand=self.scroll_barx1.set,
                                               yscrollcommand=self.scroll_bary1.set)
        self.generate_list(finished=True)
        self.scroll_bary1.pack(side="right", fill="y")
        self.scroll_barx1.pack(side="bottom", fill="x")
        self.finished_task_list.pack(side="left", fill="both")
        self.scroll_bary1.config(command=self.finished_task_list.yview)
        self.scroll_barx1.config(command=self.finished_task_list.xview)

        # finished task buttons
        self.frame5 = tk.Frame()
        self.frame5_0 = tk.Frame(master=self.frame5)
        self.frame5_1 = tk.Frame(master=self.frame5)
        self.del_finished_btn = tk.Button(master=self.frame5_0, text='Delete Task', command=lambda: self.delete_task(True))
        self.restore_finished_btn = tk.Button(master=self.frame5_0, text='Restore Task', command=lambda: self.finish_task(True))
        self.finished_lbl = tk.Label(master=self.frame5_1, text='wahaha')
        self.del_finished_btn.pack(side='left')
        self.restore_finished_btn.pack(side='left')
        self.finished_lbl.pack()
        self.frame5_0.pack()
        self.frame5_1.pack()

        # add, edit, delete button
        self.frame2 = tk.Frame()

        # add
        self.frame2_00 = tk.Frame(master=self.frame2)
        self.frame2_01 = tk.Frame(master=self.frame2)
        self.frame2_02 = tk.Frame(master=self.frame2)
        self.frame2_03 = tk.Frame(master=self.frame2)
        self.add_button = tk.Button(master=self.frame2_00, text="Add Task", command=self.add_task)
        self.add_button.pack(side='left', anchor='w')
        self.add_label_task = tk.Label(master=self.frame2_01, text="Task: ")
        self.add_label_task.pack(side='left', anchor='w')
        self.add_entry_task = tk.Entry(master=self.frame2_01, width=50)
        self.add_entry_task.pack(side='right')

        # self.add_date_task = tk.Label(master=self.frame2_02, text="Date: ")
        # self.add_date_task.pack(side='left', anchor='w')
        # self.add_entry_date = tk.Entry(master=self.frame2_02, width=50)
        # self.add_entry_date.pack(side='right')
        self.add_date_year = tk.Label(master=self.frame2_02, text="Year: ")
        self.add_date_year.pack(side='left', anchor='w')
        self.add_entry_year = tk.Entry(master=self.frame2_02, width=12)
        self.add_entry_year.pack(side='left', anchor='w')

        self.add_date_month = tk.Label(master=self.frame2_02, text=", Month: ")
        self.add_date_month.pack(side='left', anchor='w')
        self.add_entry_month = tk.Entry(master=self.frame2_02, width=11)
        self.add_entry_month.pack(side='left', anchor='w')

        self.add_date_day = tk.Label(master=self.frame2_02, text=", Day: ")
        self.add_date_day.pack(side='left', anchor='w')
        self.add_entry_day = tk.Entry(master=self.frame2_02, width=11)
        self.add_entry_day.pack(side='right')

        self.frame2_01.pack()
        self.frame2_02.pack()
        self.frame2_00.pack()
        self.frame2_03.pack(pady=10)

        # edit
        self.frame2_10 = tk.Frame(master=self.frame2)
        self.frame2_11 = tk.Frame(master=self.frame2)
        self.frame2_12 = tk.Frame(master=self.frame2)
        self.frame2_13 = tk.Frame(master=self.frame2)
        self.edit_button = tk.Button(master=self.frame2_10, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side='left', anchor='w')
        self.edit_label_task = tk.Label(master=self.frame2_11, text="Task: ")
        self.edit_label_task.pack(side='left', anchor='w')
        self.edit_entry_task = tk.Entry(master=self.frame2_11, width=50)
        self.edit_entry_task.pack(side='right')
        # self.edit_date_task = tk.Label(master=self.frame2_12, text="Date: ")
        # self.edit_date_task.pack(side='left', anchor='w')
        # self.edit_entry_date = tk.Entry(master=self.frame2_12, width=50)
        # self.edit_entry_date.pack(side='right')
        self.edit_date_year = tk.Label(master=self.frame2_12, text="Year: ")
        self.edit_date_year.pack(side='left', anchor='w')
        self.edit_entry_year = tk.Entry(master=self.frame2_12, width=12)
        self.edit_entry_year.pack(side='left', anchor='w')

        self.edit_date_month = tk.Label(master=self.frame2_12, text=", Month: ")
        self.edit_date_month.pack(side='left', anchor='w')
        self.edit_entry_month = tk.Entry(master=self.frame2_12, width=11)
        self.edit_entry_month.pack(side='left', anchor='w')

        self.edit_date_day = tk.Label(master=self.frame2_12, text=", Day: ")
        self.edit_date_day.pack(side='left', anchor='w')
        self.edit_entry_day = tk.Entry(master=self.frame2_12, width=11)
        self.edit_entry_day.pack(side='right')

        self.frame2_11.pack()
        self.frame2_12.pack()
        self.frame2_10.pack()
        self.frame2_13.pack(pady=10)

        # delete
        self.delete_button = tk.Button(master=self.frame2, text="Delete Task", command=lambda: self.delete_task(False))
        self.delete_button.pack(pady=30)

        # finish
        self.finish_button = tk.Button(master=self.frame2, text="Finish Task", command=lambda: self.finish_task(False))
        self.finish_button.pack()

        self.frame2_20 = tk.Frame(master=self.frame2)
        self.frame2_21 = tk.Frame(master=self.frame2)
        self.add_delete_edit_label = tk.Label(master=self.frame2_20, text='')
        self.add_delete_edit_label.pack()
        self.frame2_20.pack()
        self.frame2_21.pack(pady=10)

        # time tracker
        self.track_flag = False
        self.tracked_idx = -1
        self.nowTime = tk.StringVar()
        self.nowTime.set("current time: " + self.getNowTimeString())
        self.tracked_time = tk.StringVar()
        self.tracked_time.set("Duration time: " + "00:00:00")
        self.frame3 = tk.Frame()
        self.label_current_time = tk.Label(master=self.frame3, textvariable=self.nowTime)
        self.label_current_time.pack(ipady = 10)
        self.label_current_time.after(1000, self.updateTime)

        self.label_track = tk.Label(master=self.frame3, text="The current tracked task is: None.")
        self.label_track.pack(ipady = 5)
        self.timing_btn = tk.Button(master=self.frame3, text='Start Timing', command=self.time_track)
        self.timing_btn.pack(side='left', anchor='w', ipadx=5)
        self.finish_btn = tk.Button(master=self.frame3, text='Finish Timing', command=self.finish_track)
        self.finish_btn.pack(side='left', anchor='w', ipadx=5)

        self.label_tracked_time = tk.Label(master=self.frame3, textvariable=self.tracked_time)
        self.label_tracked_time.pack(ipady=10)
        self.label_tracked_time.after(1000, self.updateTrackedTime)

        self.frame30 = tk.Frame(master=self.frame3)
        self.frame30.pack()

        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=1)
        self.frame4.grid(row=1, column=0)
        self.frame5.grid(row=2, column=0)

    def generate_list(self, finished):
        sql = 'select * from date_task where FINISHED=%s'
        self.cursor.execute(sql%(finished))
        results = self.cursor.fetchall()
        if finished:
            list_to_do = self.finished_task_list
        elif not finished:
            list_to_do = self.unfinished_task_list

        list_content = []
        for i in range(len(results)):
            list_content.append(str(results[i][0])+": "+str(results[i][1]) + ", ("+str(results[i][2]) + ")")
        if not finished:
            list_content.sort()
        elif finished:
            list_content.sort(reverse=True)
        for item in list_content:
            list_to_do.insert(tk.END, item)

    def add_task_to_list_UI(self, finished, date='', task='', tracked_time='', new_task_date=''):
        if new_task_date=='':
            new_task_date = date + ": " + task + ", (" + tracked_time + ")"

        flag = False
        if finished:
            target_list = self.finished_task_list
        elif not finished:
            target_list = self.unfinished_task_list

        for i in range(target_list.size()):
            if new_task_date <= target_list.get(i) and not finished:
                target_list.insert(i, new_task_date)
                flag = True
                break
            elif new_task_date > target_list.get(i) and finished:
                target_list.insert(i, new_task_date)
                flag = True
                break
        if not flag:
            target_list.insert(tk.END, new_task_date)

    def add_task_to_DB(self, finished, date='', task='', tracked_time='', new_task_date=''):
        if new_task_date!='':
            date = new_task_date[:new_task_date.find(':')]
            task = new_task_date[new_task_date.find(':') + 2:new_task_date.find(',')]
            tracked_time = new_task_date[new_task_date.find('(') + 1:new_task_date.find(')')]

        sql = 'INSERT INTO date_task (TASK_DATE, TASK, TRACKED_TIME, FINISHED) VALUES (\'%s\', \'%s\', \'%s\', finished);'
        try:
            self.cursor.execute(sql % (date, task, tracked_time))
            self.db.commit()
        except:
            self.db.rollback()

    def del_task_from_DB(self, date='', task='', task_date=''):
        if task_date!='':
            date = task_date[:task_date.find(':')]
            task = task_date[task_date.find(':') + 2:task_date.find(',')]
        sql = 'DELETE FROM date_task WHERE TASK_DATE=\'%s\' AND TASK=\'%s\';'
        try:
            self.cursor.execute(sql % (date, task))
            self.db.commit()
        except:
            self.db.rollback()

    def alt_finished_state_DB(self, date='', task='', task_date=''):
        if task_date!='':
            date = task_date[:task_date.find(':')]
            task = task_date[task_date.find(':') + 2:task_date.find(',')]
        sql = 'select FINISHED from date_task where TASK_DATE=\'%s\' AND TASK=\'%s\''
        self.cursor.execute(sql % (date, task))
        fin_state = not bool(self.cursor.fetchall()[0][0])

        sql = 'UPDATE date_task SET FINISHED = %s WHERE TASK_DATE=\'%s\' AND TASK=\'%s\';'
        try:
            self.cursor.execute(sql % (fin_state, date, task))
            self.db.commit()
        except:
            self.db.rollback()

    def add_zero(self, str):
        if str == '':
            return ''
        elif int(str) < 10:
            return "0" + str
        else:
            return str

    def date_from_entries(self, add_edit):
        year, month, day = '', '', ''
        if add_edit == 'add':
            year, month, day = self.add_zero(self.add_entry_year.get()), self.add_zero(self.add_entry_month.get()), \
                               self.add_zero(self.add_entry_day.get())
        elif add_edit == "edit":
            year, month, day = self.add_zero(self.edit_entry_year.get()), self.add_zero(self.edit_entry_month.get()), \
                               self.add_zero(self.edit_entry_day.get())

        if year == '':
            year = strftime("%Y", gmtime())
        if month == '':
            month = strftime("%m", gmtime())
        if day == '':
            day = strftime("%d", gmtime())
        return year + "-" + month + "-" + day


    def add_task(self):
        if self.tracked_idx != -1:
            self.add_delete_edit_label['text'] = 'Please finish timing first before adding task.'
            return

        self.add_task_to_DB(finished=False, date=self.date_from_entries(add_edit='add'),
                            task=self.add_entry_task.get(), tracked_time='NA')
        self.add_task_to_list_UI(finished=False, date=self.date_from_entries(add_edit='add'),
                                 task=self.add_entry_task.get(), tracked_time='NA')
        self.add_delete_edit_label['text'] = 'Task ' + self.add_entry_task.get() + " added successfully"

        # if self.add_entry_task.get() == '' or self.add_entry_date.get() == '':
        #     self.add_delete_edit_label['text'] = 'Please input date and task if you need to add a task.'
        # else:
        #     self.add_task_to_DB(finished=False, date=self.add_entry_date.get(), task=self.add_entry_task.get(), tracked_time='NA')
        #     self.add_task_to_list_UI(finished=False, date=self.add_entry_date.get(), task=self.add_entry_task.get(), tracked_time='NA')

    def edit_task(self):
        if self.tracked_idx!=-1:
            self.add_delete_edit_label['text'] = 'Please finish timing first before editing task.'
            return

        if self.unfinished_task_list.curselection()==():
            self.add_delete_edit_label['text'] = 'You have not chosen a task to edit yet!'
        else:
            idx = self.unfinished_task_list.curselection()[0]
            self.add_delete_edit_label['text'] = ''

            if self.edit_entry_task.get()=='' and self.edit_entry_year.get()=='' and self.edit_entry_month.get()=='' and self.edit_entry_day.get()=='':
                self.add_delete_edit_label['text'] = 'Please input date or task if you need to edit a task.'
            else:
                delete_date = self.unfinished_task_list.get(idx)[:self.unfinished_task_list.get(idx).find(':')]
                delete_task = self.unfinished_task_list.get(idx)[self.unfinished_task_list.get(idx).find(':') + 2:self.unfinished_task_list.get(idx).find(',')]
                tracked_time = self.unfinished_task_list.get(idx)[self.unfinished_task_list.get(idx).find('(') + 1:self.unfinished_task_list.get(idx).find(')')]
                add_date = delete_date
                add_task = delete_task

                if self.edit_entry_year.get()=='' and self.edit_entry_month.get()=='' and self.edit_entry_day.get()=='':
                    add_task = self.edit_entry_task.get()
                elif self.edit_entry_task.get() == '':
                    add_date = self.date_from_entries(add_edit='edit')
                else:
                    add_date = self.date_from_entries(add_edit='edit')
                    add_task = self.edit_entry_task.get()
                new_task_date = add_date + ": " + add_task + ", (" + tracked_time + ")"

                self.del_task_from_DB(date=delete_date, task=delete_task)
                self.add_task_to_DB(date=add_date, task=add_task, finished=False, tracked_time=tracked_time)

                self.unfinished_task_list.delete(self.unfinished_task_list.curselection())
                self.add_task_to_list_UI(finished=False, new_task_date=new_task_date)

    def delete_task(self, finished):
        if finished:
            lbl = self.finished_lbl
            task_list = self.finished_task_list
        elif not finished:
            lbl = self.add_delete_edit_label
            task_list = self.unfinished_task_list

        if self.tracked_idx!=-1:
            lbl['text'] = 'Please finish timing first before deleting task.'
            return
        if task_list.curselection()==():
            lbl['text'] = 'You have not chosen a task to delete yet!'
        else:
            data_delete = task_list.get(task_list.curselection()[0])
            self.del_task_from_DB(task_date=data_delete)

            lbl['text'] = ''
            task_list.delete(task_list.curselection())

    def finish_task(self, finished):
        if finished:
            lbl = self.finished_lbl
            task_list = self.finished_task_list
        elif not finished:
            lbl = self.add_delete_edit_label
            task_list = self.unfinished_task_list

        if self.tracked_idx!=-1:
            lbl['text'] = 'Please finish timing first before finishing task.'
            return

        if task_list.curselection()==():
            lbl['text'] = 'You have not chosen a task to finish yet!'
        else:
            data_finish = task_list.get(task_list.curselection()[0])
            self.alt_finished_state_DB(task_date=data_finish)

            lbl['text'] = ''
            task_list.delete(task_list.curselection())
            self.add_task_to_list_UI(finished=not finished, new_task_date=data_finish)

    def updateTime(self):
        self.nowTime.set("current time: "+self.getNowTimeString())
        self.label_current_time.after(1000, self.updateTime)

    def getNowTimeString(self):
        now = dt.datetime.now()

        text = '%s-%s-%s %s:%s:%s' % \
               (now.year,
                '{:0>2d}'.format(now.month),
                '{:0>2d}'.format(now.day),
                '{:0>2d}'.format(now.hour),
                '{:0>2d}'.format(now.minute),
                '{:0>2d}'.format(now.second))
        return text

    def set_track_time(self, idx):
        data_tracked = self.unfinished_task_list.get(idx)
        date_tracked = data_tracked[:data_tracked.find(": ")]
        task_tracked = data_tracked[data_tracked.find(": ") + 2:data_tracked.find(",")]
        time_tracked = self.label_tracked_time['text'].partition(': ')[2]
        new_msg = date_tracked + ": " + task_tracked + ", (" + time_tracked + ")"

        # modify DB
        sql = 'UPDATE date_task SET TRACKED_TIME = \'%s\' WHERE TASK_DATE=\'%s\' AND TASK=\'%s\';'
        try:
            self.cursor.execute(sql % (time_tracked, date_tracked, task_tracked))
            self.db.commit()
        except:
            self.db.rollback()

        # modify UI
        self.unfinished_task_list.delete(idx)
        flag = False
        for i in range(self.unfinished_task_list.size()):
            if new_msg <= self.unfinished_task_list.get(i):
                self.unfinished_task_list.insert(i, new_msg)
                flag = True
                break
        if not flag:
            self.unfinished_task_list.insert(tk.END, new_msg)

    def time_track(self):
        if self.timing_btn['text'] == 'Start Timing':
            if self.unfinished_task_list.curselection() == ():
                self.label_track['text'] = 'You have not chosen a task to track yet!'
                self.tracked_idx = -1
            else:
                idx = self.unfinished_task_list.curselection()[0]
                self.label_track['text'] = 'The current tracked task is (tracking): ' + self.unfinished_task_list.get(
                    idx)
                self.tracked_idx = idx
                ###### needed to be changed. connect to db to obtain already tracked time
                start_time_db = self.unfinished_task_list.get(idx)[
                                self.unfinished_task_list.get(idx).find('(') + 1:self.unfinished_task_list.get(
                                    idx).find(')')]
                if start_time_db == 'NA':
                    start_time = dt.datetime(year=2021, month=1, day=1, hour=0, minute=0,
                                             second=0)  # NEEDED to be modified
                else:
                    start_time = dt.datetime(year=2021, month=1, day=1,
                                             hour=int(start_time_db[:start_time_db.find(':')]),
                                             minute=int(
                                                 start_time_db[start_time_db.find(':') + 1: start_time_db.rfind(':')]),
                                             second=int(start_time_db[start_time_db.rfind(':') + 1:]))
                text = '%s:%s:%s' % \
                       ('{:0>2d}'.format(start_time.hour),
                        '{:0>2d}'.format(start_time.minute),
                        '{:0>2d}'.format(start_time.second))
                self.tracked_time.set("Duration time: " + text)
                self.track_flag = True
                self.timing_btn['text'] = 'Pause Timing'
        elif self.timing_btn['text'] == 'Pause Timing':
            if self.tracked_idx == -1:
                self.label_track['text'] = 'You have not chosen a task to track.'
            else:
                self.track_flag = False
                self.timing_btn['text'] = 'Resume Timing'
                self.set_track_time(self.tracked_idx)
        elif self.timing_btn['text'] == 'Resume Timing':
            self.track_flag = True
            self.timing_btn['text'] = 'Pause Timing'

    def finish_track(self):
        if self.tracked_idx == -1:
            self.label_track['text'] = 'You have not chosen a task to track.'
        else:
            # update db to store finishing time
            self.set_track_time(self.tracked_idx)
            self.track_flag = False
            self.timing_btn['text'] = 'Start Timing'
            self.tracked_idx = -1
            self.tracked_time.set("Duration time: "+"00:00:00")
            self.label_track['text'] = 'The current tracked task is: None.'

    def updateTrackedTime(self):
        self.tracked_time.set("Duration time: "+self.getDurationTimeString())
        self.label_current_time.after(1000, self.updateTrackedTime)

    def getDurationTimeString(self):
        tracked_time_str = self.tracked_time.get()
        tracked_time_str = tracked_time_str.partition("Duration time: ")[2]

        h, rest = int(tracked_time_str.partition(':')[0]), tracked_time_str.partition(':')[2]
        m, rest = int(rest.partition(':')[0]), rest.partition(':')[2]
        s = int(rest)
        prev_duration = dt.datetime(year=2021, month=1, day=1, hour=h, minute=m, second=s)

        if (self.track_flag):
            next_duration = prev_duration + dt.timedelta(seconds=1)
        elif not self.track_flag:
            next_duration = prev_duration

        text = '%s:%s:%s' % \
               ('{:0>2d}'.format(next_duration.hour),
                '{:0>2d}'.format(next_duration.minute),
                '{:0>2d}'.format(next_duration.second))
        return text

if __name__ == '__main__':
    task_scheduler = task_scheduler()
    task_scheduler.mainloop()