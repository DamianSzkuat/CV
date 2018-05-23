import tkinter as tk


class ButtonContainer(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        #self.pack(side="right", fill="none", expand=True)
        self.grid(row=0, column=1, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def createImageNavigationButtons(self, controller):
        self.next_button = tk.Button(self,
                                     text="Next Image",
                                     command=lambda: controller.showNext())
        self.next_button.grid(row=0, column=1, sticky="ew", padx=(20,0))

        self.prev_button = tk.Button(self,
                                     text="Previous Image",
                                     command=lambda: controller.showPrevious())
        self.prev_button.grid(row=1, column=1, sticky="ew", pady=(0,20), padx=(20,0))

    def createFunctionButtons(self, controller):
        self.procrustes_button = tk.Button(self,
                                           text="Perform initial procrustes analysis",
                                           command=lambda: controller.performInitialProcrustes())
        self.procrustes_button.grid(row=3, column=1, sticky="ew", padx=(20,0))
    
        self.PCA_button = tk.Button(self,
                                    text="Perform PCA",
                                    command=lambda: controller.perfromPCA())
        self.PCA_button.grid(row=4, column=1, sticky="ew",padx=(20,0))

        self.Model_manual_pos_init_button = tk.Button(self,
                                                      text="Manual position initialization",
                                                      command=lambda: controller.performManualModelPositionInit())
        self.Model_manual_pos_init_button.grid(row=5, column=1, sticky="ew", padx=(20,0))
        
        self.Model_auto_pos_init_button = tk.Button(self,
                                             text="Automatic position initialization",
                                             command=lambda: controller.performAutoModelPositionInit())
        self.Model_auto_pos_init_button.grid(row=6, column=1, sticky="ew", padx=(20,0))

        self.ModelFitting_button = tk.Button(self,
                                             text="Model Fitting",
                                             command=lambda: controller.performModelFitting())
        self.ModelFitting_button.grid(row=7, column=1, sticky="ew", pady=(0,20), padx=(20,0))
    
    def createTeethSwapButtons(self, controller):
        self.teethButtonContainer = tk.Frame(self)
        self.teethButtonContainer.grid(row=9, column=1, sticky="ew", pady=(0,500), padx=(20,0))
        self.tooth_1_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 1",
                                        command= lambda: controller.showProcrustesTeethAtIndex(0))
        self.tooth_1_button.grid(row=0, column=0, sticky="ew")

        self.tooth_2_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 2",
                                        command= lambda: controller.showProcrustesTeethAtIndex(1))
        self.tooth_2_button.grid(row=0, column=1, sticky="ew")

        self.tooth_3_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 3",
                                        command= lambda: controller.showProcrustesTeethAtIndex(2))
        self.tooth_3_button.grid(row=0, column=2, sticky="ew")

        self.tooth_4_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 4",
                                        command= lambda: controller.showProcrustesTeethAtIndex(3))
        self.tooth_4_button.grid(row=0, column=3, sticky="ew")

        self.tooth_5_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 5",
                                        command= lambda: controller.showProcrustesTeethAtIndex(4))
        self.tooth_5_button.grid(row=1, column=0, sticky="ew")

        self.tooth_6_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 6",
                                        command= lambda: controller.showProcrustesTeethAtIndex(5))
        self.tooth_6_button.grid(row=1, column=1, sticky="ew")

        self.tooth_7_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 7",
                                        command= lambda: controller.showProcrustesTeethAtIndex(6))
        self.tooth_7_button.grid(row=1, column=2, sticky="ew")

        self.tooth_8_button = tk.Button(self.teethButtonContainer,
                                        text="Tooth 8",
                                        command= lambda: controller.showProcrustesTeethAtIndex(7))
        self.tooth_8_button.grid(row=1, column=3, sticky="ew")


