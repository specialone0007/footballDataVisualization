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
    public partial class Form2 : Form
    {
        public string Get(string uri)
        {
            System.Net.HttpWebRequest request = (System.Net.HttpWebRequest)System.Net.WebRequest.Create(uri);
            request.AutomaticDecompression = System.Net.DecompressionMethods.GZip | System.Net.DecompressionMethods.Deflate;

            using (System.Net.HttpWebResponse response = (System.Net.HttpWebResponse)request.GetResponse())
            using (System.IO.Stream stream = response.GetResponseStream())
            using (System.IO.StreamReader reader = new System.IO.StreamReader(stream))
            {
                return reader.ReadToEnd().Replace("\"", "");
            }
        }

        Form1 form1;
        List<string> team_names = new List<string>();
        Dictionary<string, string> important_action_dict = new Dictionary<string, string>();

        private void Form2_FormClosing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            Environment.Exit(0);
        }

        public Form2(Form1 parent)
        {
            Control.CheckForIllegalCrossThreadCalls = false;
            this.FormClosing += new FormClosingEventHandler(Form2_FormClosing);

            InitializeComponent();
            form1 = parent;

            comboBoxVisualType1.Items.Add("Xg Timing Chart");
            comboBoxVisualType1.Items.Add("Xg Nodes");
            comboBoxVisualType1.Items.Add("Important Action Heatmaps");
            comboBoxVisualType1.Items.Add("Average Positions");
            comboBoxVisualType1.Items.Add("Action Heatmaps");
            comboBoxVisualType1.Items.Add("Important Action Sequences");
            
            comboBox1.Items.Add("Xg Timing Chart");
            comboBox1.Items.Add("Xg Nodes");
            comboBox1.Items.Add("Important Action Heatmaps");
            comboBox1.Items.Add("Average Positions");
            comboBox1.Items.Add("Action Heatmaps");
            comboBox1.Items.Add("Important Action Sequences");   
        }

        private void visualTypeHandle(ComboBox visualType, ComboBox Filter1, ComboBox Filter2, ComboBox Filter3, PictureBox pictureBox)
        {
            if (!team_names.Any())
            {
                team_names = Get("http://127.0.0.1:5000/team_names").Split(',').ToList();
            }

            Filter1.Items.Clear();
            Filter2.Items.Clear();
            Filter3.Items.Clear();

            if (visualType.SelectedItem.ToString() == "Average Positions")
            {
                Filter1.Text = "Select Team";
                Filter2.Text = "Select Position Type";
                Filter3.Text = "No More Selection Needed";


                foreach (string name in team_names)
                {
                    Filter1.Items.Add(name);
                }
                Filter2.Items.Add("Out Position");
                Filter2.Items.Add("In Position");
            }
            else if (visualType.SelectedItem.ToString() == "Action Heatmaps")
            {
                Filter1.Items.Clear();
                Filter2.Items.Clear();

                Filter1.Text = "Select Team";

                foreach (string name in team_names)
                {
                    Filter1.Items.Add(name);
                }

                Filter2.Text = "Select Player";
                Filter3.Text = "Select Action Heatmap Type";
            }
            else if (visualType.SelectedItem.ToString() == "Important Action Sequences")
            {
                Filter1.Text = "Select Team";

                foreach (string name in team_names)
                {
                    Filter1.Items.Add(name);
                }
                Filter2.Text = "Select Player";
                Filter3.Text = "Select Action";
            }
            else if (visualType.SelectedItem.ToString() == "Xg Timing Chart")
            {
                Filter1.Text = "No More Selection Needed";
                Filter2.Text = "No More Selection Needed";
                Filter3.Text = "No More Selection Needed";

                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/xg_scatter");
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
            else if (visualType.SelectedItem.ToString() == "Xg Nodes")
            {
                Filter1.Text = "No More Selection Needed";
                Filter2.Text = "No More Selection Needed";
                Filter3.Text = "No More Selection Needed";

                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/xg_nodes");
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
            else if (visualType.SelectedItem.ToString() == "Important Action Heatmaps")
            {
                Filter1.Text = "Select Team";

                foreach (string name in team_names)
                {
                    Filter1.Items.Add(name);
                }

                Filter2.Text = "No More Selection Needed";
                Filter3.Text = "No More Selection Needed";
            }
        }

        private void filter1Handle(ComboBox visualType, ComboBox Filter1, ComboBox Filter2, ComboBox Filter3, PictureBox pictureBox)
        {
            if (Filter2.SelectedIndex > -1 & visualType.SelectedItem.ToString() == "Average Positions")
            {
                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/average_positions?var=" + Filter1.SelectedItem.ToString() + "-" + Filter2.SelectedItem.ToString());
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }

            else if (visualType.SelectedItem.ToString() == "Action Heatmaps")
            {
                Filter2.Items.Clear();
                Filter3.Items.Clear();
                List<string> player_names = Get("http://127.0.0.1:5000/player_names?var=" + Filter1.SelectedItem.ToString()).Split(',').ToList();
                foreach (string name in player_names)
                {
                    Filter2.Items.Add(name);
                }
                Filter2.Text = "Select Player";
                Filter3.Text = "Select Action Heatmap Type";
            }
            else if (visualType.SelectedItem.ToString() == "Important Action Sequences")
            {
                Filter2.Items.Clear();
                Filter3.Items.Clear();

                List<string> player_names = Get("http://127.0.0.1:5000/player_names?var=" + Filter1.SelectedItem.ToString()).Split(',').ToList();
                foreach (string name in player_names)
                {
                    Filter2.Items.Add(name);
                }
                Filter2.Items.Add("Continue Without Selected Player");

                Filter2.Text = "Select Player";
                Filter3.Text = "Select Action";
            }

            else if (visualType.SelectedItem.ToString() == "Important Action Heatmaps")
            {
                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/important_actions_heatmap?var=" + Filter1.SelectedItem.ToString());
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
        }

        private void filter2Handle(ComboBox visualType, ComboBox Filter1, ComboBox Filter2, ComboBox Filter3, PictureBox pictureBox)
        {
            if (visualType.SelectedItem.ToString() == "Average Positions" & Filter1.SelectedIndex > -1)
            {
                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/average_positions?var=" + Filter1.SelectedItem.ToString() + "-" + Filter2.SelectedItem.ToString());
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
            else if (visualType.SelectedItem.ToString() == "Action Heatmaps")
            {
                Filter3.Items.Clear();
                List<string> action_list = Get("http://127.0.0.1:5000/available_actions?var=" + Filter2.SelectedItem.ToString()).Split(',').ToList();
                foreach (string name in action_list)
                {
                    Filter3.Items.Add(name);
                }
                Filter3.Text = "Select Action Heatmap Type";
            }
            else if (visualType.SelectedItem.ToString() == "Important Action Sequences")
            {
                Filter3.Items.Clear();
                important_action_dict.Clear();
                string response = Get("http://127.0.0.1:5000/possible_important_actions?var=" + Filter2.SelectedItem.ToString() + "-" + Filter1.SelectedItem.ToString());


                if ('!' == response[0])
                {
                    Filter3.Text = "No Important Action Involvement Detected";
                }
                else
                {
                    List<string> action_list = response.Split(',').ToList();

                    foreach (string name in action_list)
                    {
                        string id = name.Substring(name.LastIndexOf('-') + 1);
                        string action_string = name.Substring(0, name.LastIndexOf('-'));
                        Filter3.Items.Add(action_string);
                        important_action_dict.Add(action_string, id);
                    }
                    Filter3.Text = "Select Action";
                }
            }
        }

        private void filter3Handle(ComboBox visualType, ComboBox Filter1, ComboBox Filter2, ComboBox Filter3, PictureBox pictureBox)
        {
            if (visualType.SelectedItem.ToString() == "Action Heatmaps" & Filter1.SelectedIndex > -1 & Filter2.SelectedIndex > -1)
            {
                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/action_heatmap?var=" + Filter2.SelectedItem.ToString() + "-" + Filter3.SelectedItem.ToString());
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
            else if (visualType.SelectedItem.ToString() == "Important Action Sequences" & Filter1.SelectedIndex > -1 & Filter2.SelectedIndex > -1)
            {
                pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                string pngName = Get("http://127.0.0.1:5000/important_action?var=" + important_action_dict[Filter3.SelectedItem.ToString()]);
                Bitmap MyImage = new Bitmap("Images/" + pngName);
                pictureBox.Image = (Image)MyImage;
            }
        }

        private void comboBoxVisualType1_SelectedIndexChanged(object sender, EventArgs e)
        {
            visualTypeHandle(comboBoxVisualType1, comboBoxFilterVisualization1, comboBoxFilterVisualization2, comboBoxFilterVisualization3, pictureBoxVisual1);
        }

        private void comboBoxFilterVisualization1_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter1Handle(comboBoxVisualType1, comboBoxFilterVisualization1, comboBoxFilterVisualization2, comboBoxFilterVisualization3, pictureBoxVisual1);
        }

        private void comboBoxFilterVisualization2_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter2Handle(comboBoxVisualType1, comboBoxFilterVisualization1, comboBoxFilterVisualization2, comboBoxFilterVisualization3, pictureBoxVisual1);
        }

        private void comboBoxFilterVisualization3_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter3Handle(comboBoxVisualType1, comboBoxFilterVisualization1, comboBoxFilterVisualization2, comboBoxFilterVisualization3, pictureBoxVisual1);
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            visualTypeHandle(comboBox1, comboBox2, comboBox3, comboBox4, pictureBox1);
        }

        private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter1Handle(comboBox1, comboBox2, comboBox3, comboBox4, pictureBox1);
        }

        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter2Handle(comboBox1, comboBox2, comboBox3, comboBox4, pictureBox1);
        }

        private void comboBox4_SelectedIndexChanged(object sender, EventArgs e)
        {
            filter3Handle(comboBox1, comboBox2, comboBox3, comboBox4, pictureBox1);
        }
    }
}
