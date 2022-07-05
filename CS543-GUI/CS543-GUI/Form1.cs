using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CS543_GUI
{
    public partial class Form1 : Form
    {
        Form2 form2;

        private void Form1_FormClosing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            Environment.Exit(0);
        }

        public Form1()
        {
            Control.CheckForIllegalCrossThreadCalls = false;
            this.FormClosing += new FormClosingEventHandler(Form1_FormClosing);

            InitializeComponent();
            this.Text = "Main Page";
            form2 = new Form2(this);
        }

        private void importantActions_Click(object sender, EventArgs e)
        {
            this.Hide();
            this.form2.ShowDialog();
        }
    }
}
