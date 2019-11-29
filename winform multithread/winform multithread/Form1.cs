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
        int ticks_end_time = 40;

        public Form1()
        {
            InitializeComponent();

            client = new TcpClient();
            client.Connect(new IPEndPoint(IPAddress.Parse("172.16.13.210"), 53656));
            sw = new StreamWriter(client.GetStream()); sw.AutoFlush = true;
            sr = new StreamReader(client.GetStream());
            label1.Text = "connection established";

            listBox1.Items.Add("Please eneter your name");
            
            Console.WriteLine("ok");
            backgroundWorker1.RunWorkerAsync(sr);
        }

        private void button_clicked(object sender, EventArgs e)
        {
            string msg = textBox1.Text;

            if (listBox1.Items[0].ToString() == "Which subject do you want to be testest on?" )
            {
                if (msg == "history" || msg == "History")
                {
                    listBox1.Items.Clear();
                    listBox1.Items.Add("History");
                    sw.WriteLine("SubjHistory");
                }

                else
                    listBox1.Items.Add("There is not such a subject, please try again");
            }

            else if ( listBox1.Items[0].ToString() == "Please eneter your name" )
            {
                listBox1.Items.Clear();
                listBox1.Items.Add("Which subject do you want to be testest on?");
                My_name.Text = msg;
            }

            else if ( msg== "yes hint")
            {
                if (ticks > 8)
                    sw.WriteLine(My_level.Text + "-" + listBox1.Items[1] + "-" + textBox1.Text);
                else
                    listBox1.Items.Add("Try yourself a bit more");
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
            string[] words;  string subj; string level;string ques_num; string question;


            do {

                readByteCount = sr.Read(charArray, 0, charArray.Length);

                if (readByteCount > 0) {

                    data = new string(charArray, 0, readByteCount);

                    //Invoke(new Action(() => listBox1.Items.Add("server: " + data)));
                    if (data.Contains("Right") || data.Contains("Wrong"))
                    {
                        Invoke(new Action(() => listBox1.Items.Clear()));
                        Invoke(new Action(() => listBox1.Items.Add(data)));
                    }

                    else if (data == "bye")
                    {
                        Invoke(new Action(() => label1.Text = "connection terminated"));
                        Invoke(new Action(() => listBox1.Items.Add("you lost your time, you are out")));
                        Invoke(new Action(() => textBox1.Enabled=false));
                        client.Close();
                    }

                    else if (data == "you have to choose one of the shown answers... believe me one of them is right :)")
                    {
                        Invoke(new Action(() => listBox1.Items.Add("")));
                        Invoke(new Action(() => listBox1.Items.Add(data)));
                    }

                    else if (data.Contains("givenhint") )
                    {
                        ticks_end_time = ticks_end_time + 5;
                        data = data.Split('-')[1];
                        Invoke(new Action(() => listBox1.Items.Add("")));
                        Invoke(new Action(() => listBox1.Items.Add(data)));
                    }

                    else
                    {
                        words = data.Split('-');
                        subj = words[0];
                        level = words[1];
                        ques_num = words[2];
                        question = words[3];

                        Invoke(new Action(() => My_level.Text = subj + "-" + level));
                        Invoke(new Action(() => listBox1.Items.Add(ques_num + question)));

                        for (int i = 4; i < words.Length; i++)
                        {
                            Invoke(new Action(() => listBox1.Items.Add(" ")));
                            Invoke(new Action(() => listBox1.Items.Add(words[i])));

                        }

                        ticks = 0;
                        Invoke(new Action(() => timer1.Start()));
                        



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
            if (ticks == 8)
            {
                ticks_end_time = 40;
                listBox1.Items.Add("");
                listBox1.Items.Add("I see that you are having a little trouble");
                listBox1.Items.Add("if you would like a hint send yes hint");
            }

            else if (ticks== ticks_end_time)
                {
                    sw.WriteLine("time-end-error");
                }
        }
    }
}
