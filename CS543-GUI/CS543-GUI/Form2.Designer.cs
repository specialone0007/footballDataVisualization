namespace CS543_GUI
{
    partial class Form2
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
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.bindingSource1 = new System.Windows.Forms.BindingSource(this.components);
            this.comboBoxVisualType1 = new System.Windows.Forms.ComboBox();
            this.comboBoxFilterVisualization1 = new System.Windows.Forms.ComboBox();
            this.pictureBoxVisual1 = new System.Windows.Forms.PictureBox();
            this.comboBoxFilterVisualization2 = new System.Windows.Forms.ComboBox();
            this.comboBoxFilterVisualization3 = new System.Windows.Forms.ComboBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.comboBox3 = new System.Windows.Forms.ComboBox();
            this.comboBox4 = new System.Windows.Forms.ComboBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxVisual1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // textBox1
            // 
            this.textBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox1.Location = new System.Drawing.Point(12, 14);
            this.textBox1.Name = "textBox1";
            this.textBox1.ReadOnly = true;
            this.textBox1.Size = new System.Drawing.Size(717, 30);
            this.textBox1.TabIndex = 0;
            this.textBox1.Text = "Visualization-I";
            this.textBox1.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // comboBoxVisualType1
            // 
            this.comboBoxVisualType1.AccessibleDescription = "";
            this.comboBoxVisualType1.AccessibleName = "";
            this.comboBoxVisualType1.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBoxVisualType1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBoxVisualType1.FormattingEnabled = true;
            this.comboBoxVisualType1.Location = new System.Drawing.Point(12, 67);
            this.comboBoxVisualType1.Name = "comboBoxVisualType1";
            this.comboBoxVisualType1.Size = new System.Drawing.Size(717, 33);
            this.comboBoxVisualType1.TabIndex = 4;
            this.comboBoxVisualType1.Text = "Select Visualization Type";
            this.comboBoxVisualType1.SelectedIndexChanged += new System.EventHandler(this.comboBoxVisualType1_SelectedIndexChanged);
            // 
            // comboBoxFilterVisualization1
            // 
            this.comboBoxFilterVisualization1.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.comboBoxFilterVisualization1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBoxFilterVisualization1.FormattingEnabled = true;
            this.comboBoxFilterVisualization1.Location = new System.Drawing.Point(12, 125);
            this.comboBoxFilterVisualization1.Name = "comboBoxFilterVisualization1";
            this.comboBoxFilterVisualization1.Size = new System.Drawing.Size(717, 33);
            this.comboBoxFilterVisualization1.TabIndex = 5;
            this.comboBoxFilterVisualization1.Text = "Filter Visualization 1";
            this.comboBoxFilterVisualization1.SelectedIndexChanged += new System.EventHandler(this.comboBoxFilterVisualization1_SelectedIndexChanged);
            // 
            // pictureBoxVisual1
            // 
            this.pictureBoxVisual1.Location = new System.Drawing.Point(12, 294);
            this.pictureBoxVisual1.Name = "pictureBoxVisual1";
            this.pictureBoxVisual1.Size = new System.Drawing.Size(717, 482);
            this.pictureBoxVisual1.TabIndex = 6;
            this.pictureBoxVisual1.TabStop = false;
            // 
            // comboBoxFilterVisualization2
            // 
            this.comboBoxFilterVisualization2.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBoxFilterVisualization2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBoxFilterVisualization2.FormattingEnabled = true;
            this.comboBoxFilterVisualization2.Location = new System.Drawing.Point(12, 184);
            this.comboBoxFilterVisualization2.Name = "comboBoxFilterVisualization2";
            this.comboBoxFilterVisualization2.Size = new System.Drawing.Size(717, 33);
            this.comboBoxFilterVisualization2.TabIndex = 7;
            this.comboBoxFilterVisualization2.Text = "Filter Visualization 2";
            this.comboBoxFilterVisualization2.SelectedIndexChanged += new System.EventHandler(this.comboBoxFilterVisualization2_SelectedIndexChanged);
            // 
            // comboBoxFilterVisualization3
            // 
            this.comboBoxFilterVisualization3.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBoxFilterVisualization3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBoxFilterVisualization3.FormattingEnabled = true;
            this.comboBoxFilterVisualization3.Location = new System.Drawing.Point(12, 236);
            this.comboBoxFilterVisualization3.Name = "comboBoxFilterVisualization3";
            this.comboBoxFilterVisualization3.Size = new System.Drawing.Size(717, 33);
            this.comboBoxFilterVisualization3.TabIndex = 8;
            this.comboBoxFilterVisualization3.Text = "Filter Visualization 3";
            this.comboBoxFilterVisualization3.SelectedIndexChanged += new System.EventHandler(this.comboBoxFilterVisualization3_SelectedIndexChanged);
            // 
            // textBox2
            // 
            this.textBox2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox2.Location = new System.Drawing.Point(768, 14);
            this.textBox2.Name = "textBox2";
            this.textBox2.ReadOnly = true;
            this.textBox2.Size = new System.Drawing.Size(717, 30);
            this.textBox2.TabIndex = 9;
            this.textBox2.Text = "Visualization-II";
            this.textBox2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // comboBox1
            // 
            this.comboBox1.DropDownWidth = 319;
            this.comboBox1.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBox1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Location = new System.Drawing.Point(768, 67);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(717, 33);
            this.comboBox1.TabIndex = 10;
            this.comboBox1.Text = "Select Visualization Type";
            this.comboBox1.SelectedIndexChanged += new System.EventHandler(this.comboBox1_SelectedIndexChanged);
            // 
            // comboBox2
            // 
            this.comboBox2.DropDownWidth = 319;
            this.comboBox2.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBox2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Location = new System.Drawing.Point(768, 125);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(717, 33);
            this.comboBox2.TabIndex = 11;
            this.comboBox2.Text = "Filter Visualization 1";
            this.comboBox2.SelectedIndexChanged += new System.EventHandler(this.comboBox2_SelectedIndexChanged);
            // 
            // comboBox3
            // 
            this.comboBox3.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBox3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox3.FormattingEnabled = true;
            this.comboBox3.Location = new System.Drawing.Point(768, 184);
            this.comboBox3.Name = "comboBox3";
            this.comboBox3.Size = new System.Drawing.Size(717, 33);
            this.comboBox3.TabIndex = 12;
            this.comboBox3.Text = "Filter Visualization 2";
            this.comboBox3.SelectedIndexChanged += new System.EventHandler(this.comboBox3_SelectedIndexChanged);
            // 
            // comboBox4
            // 
            this.comboBox4.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.comboBox4.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.comboBox4.FormattingEnabled = true;
            this.comboBox4.Location = new System.Drawing.Point(768, 236);
            this.comboBox4.Name = "comboBox4";
            this.comboBox4.Size = new System.Drawing.Size(717, 33);
            this.comboBox4.TabIndex = 13;
            this.comboBox4.Text = "Filter Visualization 3";
            this.comboBox4.SelectedIndexChanged += new System.EventHandler(this.comboBox4_SelectedIndexChanged);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(768, 294);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(717, 482);
            this.pictureBox1.TabIndex = 14;
            this.pictureBox1.TabStop = false;
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1924, 993);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.comboBox4);
            this.Controls.Add(this.comboBox3);
            this.Controls.Add(this.comboBox2);
            this.Controls.Add(this.comboBox1);
            this.Controls.Add(this.textBox2);
            this.Controls.Add(this.comboBoxFilterVisualization3);
            this.Controls.Add(this.comboBoxFilterVisualization2);
            this.Controls.Add(this.pictureBoxVisual1);
            this.Controls.Add(this.comboBoxFilterVisualization1);
            this.Controls.Add(this.comboBoxVisualType1);
            this.Controls.Add(this.textBox1);
            this.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Name = "Form2";
            this.Text = "Important Action Visualizations";
            ((System.ComponentModel.ISupportInitialize)(this.bindingSource1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxVisual1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.BindingSource bindingSource1;
        private System.Windows.Forms.ComboBox comboBoxVisualType1;
        private System.Windows.Forms.ComboBox comboBoxFilterVisualization1;
        private System.Windows.Forms.PictureBox pictureBoxVisual1;
        private System.Windows.Forms.ComboBox comboBoxFilterVisualization2;
        private System.Windows.Forms.ComboBox comboBoxFilterVisualization3;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.ComboBox comboBox3;
        private System.Windows.Forms.ComboBox comboBox4;
        private System.Windows.Forms.PictureBox pictureBox1;
    }
}