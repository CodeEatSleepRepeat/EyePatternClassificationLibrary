namespace EyeTrackerDataScrapper
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.panelCode = new System.Windows.Forms.Panel();
            this.panelAnswer = new System.Windows.Forms.Panel();
            this.checkBoxD = new System.Windows.Forms.CheckBox();
            this.checkBoxC = new System.Windows.Forms.CheckBox();
            this.checkBoxB = new System.Windows.Forms.CheckBox();
            this.checkBoxA = new System.Windows.Forms.CheckBox();
            this.panelBtnBack = new System.Windows.Forms.Panel();
            this.btnBack = new System.Windows.Forms.Button();
            this.panelBtnNext = new System.Windows.Forms.Panel();
            this.btnNext = new System.Windows.Forms.Button();
            this.fullPanel = new System.Windows.Forms.Panel();
            this.panelQuestion = new System.Windows.Forms.Panel();
            this.txtQuestion = new System.Windows.Forms.Label();
            this.panelAnswer.SuspendLayout();
            this.panelBtnBack.SuspendLayout();
            this.panelBtnNext.SuspendLayout();
            this.fullPanel.SuspendLayout();
            this.panelQuestion.SuspendLayout();
            this.SuspendLayout();
            // 
            // panelCode
            // 
            this.panelCode.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panelCode.AutoSize = true;
            this.panelCode.BackColor = System.Drawing.Color.WhiteSmoke;
            this.panelCode.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.panelCode.Location = new System.Drawing.Point(100, 180);
            this.panelCode.Name = "panelCode";
            this.panelCode.Size = new System.Drawing.Size(1380, 370);
            this.panelCode.TabIndex = 1;
            // 
            // panelAnswer
            // 
            this.panelAnswer.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.panelAnswer.AutoSize = true;
            this.panelAnswer.BackColor = System.Drawing.Color.WhiteSmoke;
            this.panelAnswer.Controls.Add(this.checkBoxD);
            this.panelAnswer.Controls.Add(this.checkBoxC);
            this.panelAnswer.Controls.Add(this.checkBoxB);
            this.panelAnswer.Controls.Add(this.checkBoxA);
            this.panelAnswer.Location = new System.Drawing.Point(100, 630);
            this.panelAnswer.Name = "panelAnswer";
            this.panelAnswer.Size = new System.Drawing.Size(646, 190);
            this.panelAnswer.TabIndex = 2;
            // 
            // checkBoxD
            // 
            this.checkBoxD.AutoSize = true;
            this.checkBoxD.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxD.Location = new System.Drawing.Point(25, 145);
            this.checkBoxD.Name = "checkBoxD";
            this.checkBoxD.Size = new System.Drawing.Size(54, 24);
            this.checkBoxD.TabIndex = 4;
            this.checkBoxD.Text = "(D) ";
            this.checkBoxD.UseVisualStyleBackColor = true;
            this.checkBoxD.CheckedChanged += new System.EventHandler(this.checkBoxD_CheckedChanged);
            // 
            // checkBoxC
            // 
            this.checkBoxC.AutoSize = true;
            this.checkBoxC.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxC.Location = new System.Drawing.Point(25, 105);
            this.checkBoxC.Name = "checkBoxC";
            this.checkBoxC.Size = new System.Drawing.Size(53, 24);
            this.checkBoxC.TabIndex = 3;
            this.checkBoxC.Text = "(C) ";
            this.checkBoxC.UseVisualStyleBackColor = true;
            this.checkBoxC.CheckedChanged += new System.EventHandler(this.checkBoxC_CheckedChanged);
            // 
            // checkBoxB
            // 
            this.checkBoxB.AutoSize = true;
            this.checkBoxB.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxB.Location = new System.Drawing.Point(25, 65);
            this.checkBoxB.Name = "checkBoxB";
            this.checkBoxB.Size = new System.Drawing.Size(53, 24);
            this.checkBoxB.TabIndex = 2;
            this.checkBoxB.Text = "(B) ";
            this.checkBoxB.UseVisualStyleBackColor = true;
            this.checkBoxB.CheckedChanged += new System.EventHandler(this.checkBoxB_CheckedChanged);
            // 
            // checkBoxA
            // 
            this.checkBoxA.AutoSize = true;
            this.checkBoxA.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxA.Location = new System.Drawing.Point(25, 25);
            this.checkBoxA.Name = "checkBoxA";
            this.checkBoxA.Size = new System.Drawing.Size(53, 24);
            this.checkBoxA.TabIndex = 1;
            this.checkBoxA.Text = "(A) ";
            this.checkBoxA.UseVisualStyleBackColor = true;
            this.checkBoxA.CheckedChanged += new System.EventHandler(this.checkBoxA_CheckedChanged);
            // 
            // panelBtnBack
            // 
            this.panelBtnBack.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.panelBtnBack.AutoSize = true;
            this.panelBtnBack.BackColor = System.Drawing.Color.WhiteSmoke;
            this.panelBtnBack.Controls.Add(this.btnBack);
            this.panelBtnBack.Location = new System.Drawing.Point(1040, 730);
            this.panelBtnBack.Name = "panelBtnBack";
            this.panelBtnBack.Size = new System.Drawing.Size(160, 90);
            this.panelBtnBack.TabIndex = 5;
            // 
            // btnBack
            // 
            this.btnBack.AutoSize = true;
            this.btnBack.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnBack.Location = new System.Drawing.Point(25, 30);
            this.btnBack.Name = "btnBack";
            this.btnBack.Size = new System.Drawing.Size(120, 30);
            this.btnBack.TabIndex = 0;
            this.btnBack.Text = "PRETHODNO";
            this.btnBack.UseVisualStyleBackColor = true;
            this.btnBack.Visible = false;
            this.btnBack.Click += new System.EventHandler(this.btnBack_Click);
            // 
            // panelBtnNext
            // 
            this.panelBtnNext.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.panelBtnNext.AutoSize = true;
            this.panelBtnNext.BackColor = System.Drawing.Color.WhiteSmoke;
            this.panelBtnNext.Controls.Add(this.btnNext);
            this.panelBtnNext.Location = new System.Drawing.Point(1320, 730);
            this.panelBtnNext.Name = "panelBtnNext";
            this.panelBtnNext.Size = new System.Drawing.Size(160, 90);
            this.panelBtnNext.TabIndex = 6;
            // 
            // btnNext
            // 
            this.btnNext.AutoSize = true;
            this.btnNext.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnNext.Location = new System.Drawing.Point(25, 30);
            this.btnNext.Name = "btnNext";
            this.btnNext.Size = new System.Drawing.Size(110, 30);
            this.btnNext.TabIndex = 7;
            this.btnNext.Text = "SLEDEĆE";
            this.btnNext.UseVisualStyleBackColor = true;
            this.btnNext.Click += new System.EventHandler(this.btnNext_Click);
            // 
            // fullPanel
            // 
            this.fullPanel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.fullPanel.AutoSize = true;
            this.fullPanel.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.fullPanel.Controls.Add(this.panelBtnNext);
            this.fullPanel.Controls.Add(this.panelBtnBack);
            this.fullPanel.Controls.Add(this.panelAnswer);
            this.fullPanel.Controls.Add(this.panelCode);
            this.fullPanel.Controls.Add(this.panelQuestion);
            this.fullPanel.Location = new System.Drawing.Point(0, 0);
            this.fullPanel.Name = "fullPanel";
            this.fullPanel.Size = new System.Drawing.Size(1780, 1060);
            this.fullPanel.TabIndex = 0;
            // 
            // panelQuestion
            // 
            this.panelQuestion.AutoSize = true;
            this.panelQuestion.BackColor = System.Drawing.Color.WhiteSmoke;
            this.panelQuestion.Controls.Add(this.txtQuestion);
            this.panelQuestion.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.panelQuestion.Location = new System.Drawing.Point(100, 40);
            this.panelQuestion.Name = "panelQuestion";
            this.panelQuestion.Size = new System.Drawing.Size(1040, 60);
            this.panelQuestion.TabIndex = 0;
            // 
            // txtQuestion
            // 
            this.txtQuestion.AutoSize = true;
            this.txtQuestion.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtQuestion.Location = new System.Drawing.Point(22, 21);
            this.txtQuestion.Name = "txtQuestion";
            this.txtQuestion.Size = new System.Drawing.Size(0, 20);
            this.txtQuestion.TabIndex = 0;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.ClientSize = new System.Drawing.Size(1584, 861);
            this.Controls.Add(this.fullPanel);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "Eye Tracker Test";
            this.panelAnswer.ResumeLayout(false);
            this.panelAnswer.PerformLayout();
            this.panelBtnBack.ResumeLayout(false);
            this.panelBtnBack.PerformLayout();
            this.panelBtnNext.ResumeLayout(false);
            this.panelBtnNext.PerformLayout();
            this.fullPanel.ResumeLayout(false);
            this.fullPanel.PerformLayout();
            this.panelQuestion.ResumeLayout(false);
            this.panelQuestion.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Panel panelCode;
        private System.Windows.Forms.Panel panelAnswer;
        private System.Windows.Forms.CheckBox checkBoxD;
        private System.Windows.Forms.CheckBox checkBoxC;
        private System.Windows.Forms.CheckBox checkBoxB;
        private System.Windows.Forms.CheckBox checkBoxA;
        private System.Windows.Forms.Panel panelBtnBack;
        private System.Windows.Forms.Button btnBack;
        private System.Windows.Forms.Panel panelBtnNext;
        private System.Windows.Forms.Button btnNext;
        private System.Windows.Forms.Panel fullPanel;
        private System.Windows.Forms.Panel panelQuestion;
        private System.Windows.Forms.Label txtQuestion;
    }
}

