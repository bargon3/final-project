using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Net;
using System.IO;
using System.Threading;

namespace winform_multithread
{
    public partial class Form1 : Form
    {
        TcpClient client; // socket client
        StreamWriter sw;  // streamWriter
        StreamReader sr;  // streamReader
        char[] charArray = new char[100]; // read char array
        int ticks;

        public Form1()
        {
            InitializeComponent();

            client = new TcpClient();
            client.Connect(new IPEndPoint(IPAddress.Parse("192.168.1.30"), 56923));
            sw = new StreamWriter(client.GetStream()); sw.AutoFlush = true;
            sr = new StreamReader(client.GetStream());
            label1.Text = "connection established";

            listBox1.Items.Add("Please eneter your name");
            
            Console.WriteLine("ok");
            timer1.Start();
            backgroundWorker1.RunWorkerAsync(sr);
        }

        private void button_clicked(object sender, EventArgs e)
        {
            ticks = 0;
            timer1.Start();
            string msg = textBox1.Text;
            listBox1.Items.Add("my msg :" + msg);

            if (msg.Contains("History") )
            {
                listBox1.Items.Clear();
                listBox1.Items.Add("History");
                sw.WriteLine("SubjHistory");
                
            }  
            else if ( listBox1.Items[0].ToString().Contains ("Please eneter your name") )
            {
                listBox1.Items.Clear();
                listBox1.Items.Add("Which subject do you want to be testest on?");
                My_name.Text = msg;
            }
            else
                sw.WriteLine(My_level.Text+ "-" + listBox1.Items[1]+ "-" + textBox1.Text);

            textBox1.Text = "";

        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e) // receive msg
        {
            StreamReader sr = e.Argument as StreamReader; // get streamReader argument from runWorkerAsync
            var data = "";
            var readByteCount = 0;
            string[] words; string subj; string level;string ques_num; string question;


            do {

                readByteCount = sr.Read(charArray, 0, charArray.Length);

                if (readByteCount > 0) {

                    data = new string(charArray, 0, readByteCount);

                    //Invoke(new Action(() => listBox1.Items.Add("server: " + data)));
                    if (data.Contains("Right") || data.Contains("Wrong"))
                    {
                        Invoke(new Action(() => listBox1.Items.Clear()));
                        Invoke(new Action(() => listBox1.Items.Add(data+"...")));
                    }

                    else
                    {    
                        words = data.Split('-');
                        subj = words[0];
                        level = words[1];
                        ques_num = words[2];
                        question = words[3];

                        Invoke(new Action(() => My_level.Text = subj + "-" + level));
                        Invoke(new Action(() => listBox1.Items.Add(ques_num + question )));

                        for (int i = 4; i < words.Length; i++)
                        {
                            Invoke(new Action(() => listBox1.Items.Add(" ")));
                            Invoke(new Action(() => listBox1.Items.Add(words[i])));

                        }
    

                    }



                }
                else Thread.Sleep(100);
                Console.WriteLine(data);
                }   
            while (data != "bye");
            Invoke(new Action(() => label1.Text = "connection terminated"));
        }

        private void backgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e) {
            client.Close();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            ticks++;
            if (ticks==20)
                {
                    sw.WriteLine("20-seconds");
                    listBox1.Items.Add("dude your time");
                }
        }
    }
}
