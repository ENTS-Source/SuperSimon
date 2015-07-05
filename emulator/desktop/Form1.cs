using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SuperSimonEmulator
{
    public partial class Form1 : Form
    {
        private delegate void delVoidInt(int i);

        private bool _on = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            spTeensy.Open();
            spTeensy.DataReceived += spTeensy_DataReceived;
        }

        private void spTeensy_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            while (spTeensy.BytesToRead > 0)
            {
                int b = spTeensy.ReadByte();
                Invoke(new delVoidInt(AppendByte), b);
            }
        }

        private void AppendByte(int b)
        {
            tbLog.AppendText(b.ToString());
        }

        private void btnToggle_Click(object sender, EventArgs e)
        {
            byte command = (byte)(_on ? 0x0 : 0x1);
            _on = !_on;
            byte[] data = { command, 0x2 };
            spTeensy.Write(data, 0, data.Length);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            byte[] data = { 0x2, 0x2 };
            spTeensy.Write(data, 0, data.Length);
        }
    }
}
