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
        self.ModelFitting_button.grid(row=7, column=1, sticky="ew", pady=(0,500), padx=(20,0))


