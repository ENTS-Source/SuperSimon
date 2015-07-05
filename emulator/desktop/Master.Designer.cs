namespace SuperSimonEmulator
{
    partial class Master
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
            this.components = new System.ComponentModel.Container();
            System.Windows.Forms.GroupBox groupBox1;
            System.Windows.Forms.Label label1;
            System.Windows.Forms.Label label2;
            System.Windows.Forms.Label label3;
            this.tbLog = new System.Windows.Forms.TextBox();
            this.spTeensy = new System.IO.Ports.SerialPort(this.components);
            this.gbNewPad = new System.Windows.Forms.GroupBox();
            this.nudAddress = new System.Windows.Forms.NumericUpDown();
            this.btnNewPad = new System.Windows.Forms.Button();
            this.gpCommunication = new System.Windows.Forms.GroupBox();
            this.cbPort = new System.Windows.Forms.ComboBox();
            this.btnSpConfigure = new System.Windows.Forms.Button();
            groupBox1 = new System.Windows.Forms.GroupBox();
            label1 = new System.Windows.Forms.Label();
            label2 = new System.Windows.Forms.Label();
            label3 = new System.Windows.Forms.Label();
            groupBox1.SuspendLayout();
            this.gbNewPad.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nudAddress)).BeginInit();
            this.gpCommunication.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(this.tbLog);
            groupBox1.Dock = System.Windows.Forms.DockStyle.Bottom;
            groupBox1.Location = new System.Drawing.Point(0, 95);
            groupBox1.Name = "groupBox1";
            groupBox1.Size = new System.Drawing.Size(585, 131);
            groupBox1.TabIndex = 3;
            groupBox1.TabStop = false;
            groupBox1.Text = "Raw Communication";
            // 
            // tbLog
            // 
            this.tbLog.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tbLog.Font = new System.Drawing.Font("Lucida Console", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tbLog.Location = new System.Drawing.Point(3, 16);
            this.tbLog.Multiline = true;
            this.tbLog.Name = "tbLog";
            this.tbLog.ReadOnly = true;
            this.tbLog.Size = new System.Drawing.Size(579, 112);
            this.tbLog.TabIndex = 0;
            // 
            // spTeensy
            // 
            this.spTeensy.PortName = "COM6";
            this.spTeensy.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.spTeensy_DataReceived);
            // 
            // gbNewPad
            // 
            this.gbNewPad.Controls.Add(this.btnNewPad);
            this.gbNewPad.Controls.Add(this.nudAddress);
            this.gbNewPad.Controls.Add(label1);
            this.gbNewPad.Location = new System.Drawing.Point(12, 12);
            this.gbNewPad.Name = "gbNewPad";
            this.gbNewPad.Size = new System.Drawing.Size(140, 77);
            this.gbNewPad.TabIndex = 4;
            this.gbNewPad.TabStop = false;
            this.gbNewPad.Text = "New game pad";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new System.Drawing.Point(7, 20);
            label1.Name = "label1";
            label1.Size = new System.Drawing.Size(48, 13);
            label1.TabIndex = 0;
            label1.Text = "Address:";
            // 
            // nudAddress
            // 
            this.nudAddress.Location = new System.Drawing.Point(61, 18);
            this.nudAddress.Maximum = new decimal(new int[] {
            255,
            0,
            0,
            0});
            this.nudAddress.Name = "nudAddress";
            this.nudAddress.Size = new System.Drawing.Size(64, 20);
            this.nudAddress.TabIndex = 1;
            // 
            // btnNewPad
            // 
            this.btnNewPad.Location = new System.Drawing.Point(10, 44);
            this.btnNewPad.Name = "btnNewPad";
            this.btnNewPad.Size = new System.Drawing.Size(115, 23);
            this.btnNewPad.TabIndex = 2;
            this.btnNewPad.Text = "Create";
            this.btnNewPad.UseVisualStyleBackColor = true;
            this.btnNewPad.Click += new System.EventHandler(this.btnNewPad_Click);
            // 
            // gpCommunication
            // 
            this.gpCommunication.Controls.Add(this.btnSpConfigure);
            this.gpCommunication.Controls.Add(this.cbPort);
            this.gpCommunication.Controls.Add(label3);
            this.gpCommunication.Controls.Add(label2);
            this.gpCommunication.Location = new System.Drawing.Point(159, 13);
            this.gpCommunication.Name = "gpCommunication";
            this.gpCommunication.Size = new System.Drawing.Size(226, 76);
            this.gpCommunication.TabIndex = 5;
            this.gpCommunication.TabStop = false;
            this.gpCommunication.Text = "Communication";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new System.Drawing.Point(7, 23);
            label2.Name = "label2";
            label2.Size = new System.Drawing.Size(29, 13);
            label2.TabIndex = 0;
            label2.Text = "Port:";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new System.Drawing.Point(7, 43);
            label3.Name = "label3";
            label3.Size = new System.Drawing.Size(86, 13);
            label3.TabIndex = 1;
            label3.Text = "Using 9600/8N1";
            // 
            // cbPort
            // 
            this.cbPort.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbPort.FormattingEnabled = true;
            this.cbPort.Location = new System.Drawing.Point(42, 16);
            this.cbPort.Name = "cbPort";
            this.cbPort.Size = new System.Drawing.Size(178, 21);
            this.cbPort.TabIndex = 2;
            // 
            // btnSpConfigure
            // 
            this.btnSpConfigure.Location = new System.Drawing.Point(145, 47);
            this.btnSpConfigure.Name = "btnSpConfigure";
            this.btnSpConfigure.Size = new System.Drawing.Size(75, 23);
            this.btnSpConfigure.TabIndex = 3;
            this.btnSpConfigure.Text = "Configure";
            this.btnSpConfigure.UseVisualStyleBackColor = true;
            this.btnSpConfigure.Click += new System.EventHandler(this.btnSpConfigure_Click);
            // 
            // Master
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(585, 226);
            this.Controls.Add(this.gpCommunication);
            this.Controls.Add(this.gbNewPad);
            this.Controls.Add(groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Name = "Master";
            this.Text = "ENTS Simon Game Pad Emulator";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.VisibleChanged += new System.EventHandler(this.Master_VisibleChanged);
            groupBox1.ResumeLayout(false);
            groupBox1.PerformLayout();
            this.gbNewPad.ResumeLayout(false);
            this.gbNewPad.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nudAddress)).EndInit();
            this.gpCommunication.ResumeLayout(false);
            this.gpCommunication.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.IO.Ports.SerialPort spTeensy;
        private System.Windows.Forms.TextBox tbLog;
        private System.Windows.Forms.GroupBox gbNewPad;
        private System.Windows.Forms.Button btnNewPad;
        private System.Windows.Forms.NumericUpDown nudAddress;
        private System.Windows.Forms.Button btnSpConfigure;
        private System.Windows.Forms.ComboBox cbPort;
        private System.Windows.Forms.GroupBox gpCommunication;
    }
}

