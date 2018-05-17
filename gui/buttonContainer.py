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

    def createProcrustedButton(self, controller):
        self.procrustes_button = tk.Button(self,
                                           text="Perform initial procrustes analysis",
                                           command=lambda: controller.performInitialProcrustes())
        self.procrustes_button.grid(row=3, column=1, sticky="ew", padx=(20,0))
    
    def createPCAButton(self, controller):
        self.PCA_button = tk.Button(self,
                                    text="Perform PCA",
                                    command=lambda: controller.perfromPCA())
        self.PCA_button.grid(row=4, column=1, sticky="ew", pady=(0,500), padx=(20,0))