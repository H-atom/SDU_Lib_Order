package com.example.order;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.util.HashMap;
import java.util.Map;
import java.util.TimerTask;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

public class MainActivity extends AppCompatActivity {

    @SuppressLint({"UseSwitchCompatOrMaterialCode", "SetJavaScriptEnabled"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initPython();
        EditText username = findViewById(R.id.editTextNumber);
        EditText password = findViewById(R.id.editTextTextPassword);
        EditText orderId = findViewById(R.id.editTextId);
        Button search = findViewById(R.id.Search);
        Button back = findViewById(R.id.buttonBack);
        Button order = findViewById(R.id.buttonOrder);
        Button sure = findViewById(R.id.buttonSure);
        TextView contents = findViewById(R.id.contents);
        TextView searchView = findViewById(R.id.textViewSearch);
        Switch switch1 = findViewById(R.id.switch1);
        WebView webView = findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("file:///android_asset/h.html");

        String userid= CommonUtil.getSettingNote(MainActivity.this, "userinfo", "username");
        String userpwd= CommonUtil.getSettingNote(MainActivity.this, "userinfo", "password");
        if (userid!=null && userpwd!=null){
            username.setText(userid);
            password.setText(userpwd);
        }
        sure.setOnClickListener(view -> {
            if (username.getText().toString().isEmpty() || password.getText().toString().isEmpty()){
                System.out.println("123255");
                Toast.makeText(MainActivity.this,"请先输入账号或密码！",Toast.LENGTH_SHORT).show();
            }else {
                Map<String, String> map = new HashMap<String, String>(); //本地保存数据
                map.put("username", username.getText().toString());
                map.put("password", password.getText().toString());
                CommonUtil.saveSettingNote(MainActivity.this, "userinfo", map);//参数（上下文，userinfo为文件名，需要保存的数据）
            }
        });

        AtomicInteger time = new AtomicInteger();
        time.set(0);
        AtomicInteger ord= new AtomicInteger();
        AtomicReference<String> roomID = new AtomicReference<>("");
        contents.setText(callStart(0));
        AtomicBoolean bool = new AtomicBoolean(true);


        switch1.setOnCheckedChangeListener((compoundButton, b) -> {
            bool.set(true);
            if (b){
                compoundButton.setText("明天");
                time.set(1);
                contents.setText(callStart(1));
            }else {
                compoundButton.setText("今天");
                time.set(0);
                contents.setText(callStart(0));
            }
        });
        search.setOnClickListener(view -> {//查询座位情况
            int i = 0;
            if (orderId.getText().toString().equals("")) {
                searchView.setText("请输入内容");
                i = 1;
            } else if (orderId.getText().toString().equals("0")) {
                if (username.getText().toString().isEmpty() || password.getText().toString().isEmpty()) {
                    searchView.setText("学号或密码为空");
                    i = 1;
                } else {
                    String lt = back();
                    String temp = username.getText().toString()+password.getText().toString()+lt+",1,2,3";
                    webView.evaluateJavascript("javascript:strEnc(\"" + temp + "\")", s -> {
                        String book = book(username.getText().toString(), password.getText().toString(), time.get(), roomID.get(),
                                orderId.getText().toString(), 1,s,lt);
                        searchView.setText(book);
                    });
                }
            } else {
                if (bool.get()){
                    String space = space(time.get(), orderId.getText().toString());
                    if (space != null) {
                        roomID.set(orderId.getText().toString());;
                        contents.setText(space);
                        searchView.setText("输入你想预约座位的编号");
                        ord.set(1);
                    } else {
                        searchView.setText("查询失败");
                        i = 1;
                    }
                    bool.set(false);
                }
            }
            if (i == 1) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            Thread.sleep(2000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        MainActivity.this.runOnUiThread(new TimerTask() {
                            @Override
                            public void run() {
                                if (ord.get() == 1) {
                                    searchView.setText("输入你想预约座位的编号");
                                } else {
                                    searchView.setText("输入你想预约位置的编号，若选择随机，则输入零");
                                }
                            }
                        });
                    }
                }).start();
            }
        });
        order.setOnClickListener(view -> {//预约座位
            int i=0;
            if (ord.get()==0){
                searchView.setText("请先输入房间编号");
                i=1;
            }else {
                if (username.getText().toString().isEmpty()||password.getText().toString().isEmpty()){
                    searchView.setText("学号或密码为空");
                    i=1;
                }else if (orderId.getText().toString().isEmpty()) {
                    searchView.setText("请输入内容");
                    i=1;
                }else {
                    String lt = back();
                    String temp = username.getText().toString()+password.getText().toString()+lt+",1,2,3";
                    webView.evaluateJavascript("javascript:strEnc(\"" + temp + "\")", s -> {
                        String book = book(username.getText().toString(), password.getText().toString(), time.get(), roomID.get(),
                                orderId.getText().toString(), 0, s,lt);
                        searchView.setText(book);
                    });
                }
            }
            if (i==1){
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            Thread.sleep(2000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        MainActivity.this.runOnUiThread(new TimerTask() {
                            @Override
                            public void run() {
                                if (ord.get() == 1) {
                                    searchView.setText("输入你想预约座位的编号");
                                } else {
                                    searchView.setText("输入你想预约位置的编号，若选择随机，则输入零");
                                }
                            }
                        });
                    }
                }).start();
            }
        });

        back.setOnClickListener(view -> {//返回按钮
            bool.set(true);
            if (ord.get()==1){
                contents.setText(callStart(time.get()));
                ord.set(0);
                searchView.setText("输入你想预约位置的编号，若选择随机，则输入零");
            }else {
                searchView.setText("已不能再返回");
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            Thread.sleep(2000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        MainActivity.this.runOnUiThread(new TimerTask() {
                            @Override
                            public void run() {
                                searchView.setText("输入你想预约位置的编号，若选择随机，则输入零");
                            }
                        });
                    }
                }).start();
            }
        });


    }

    void initPython(){
        if (!Python.isStarted()){
            Python.start(new AndroidPlatform(this));
        }
    }

    public String callStart(int i){
        Python py = Python.getInstance();
        PyObject pyObject = py.getModule("Library").callAttr("room_lists",i,0);
        return pyObject.toString();
    }

    public String book(String username, String password, int i, String number, String id, int is_random, String strEnc, String lt){
        Python py = Python.getInstance();
        PyObject pyObject =py.getModule("Library").callAttr("book",i,number,id,username,password,is_random,strEnc,lt);
        return pyObject.toString();
    }
    public String space(int i, String number){
        Python py = Python.getInstance();
        PyObject pyObject =py.getModule("Library").callAttr("space_lists",i,number,0);
        return pyObject.toString();
    }

    public String back(){
        Python py = Python.getInstance();
        PyObject pyObject =py.getModule("Library").callAttr("back");
        return pyObject.toString();
    }
}