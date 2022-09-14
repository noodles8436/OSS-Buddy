package com.example.realbusdriver;

import android.app.AlertDialog;
import android.content.Intent;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    Button joinpass;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        joinpass=(Button) findViewById(R.id.joinbox);
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        NetworkBus.start();
        joinpass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, JoinActivity.class);
                startActivity(intent);
            }
        });
    }
    public void btn_Click(View view) {
        TextView test1 = (TextView) findViewById(R.id.test1);
        EditText busid = (EditText) findViewById(R.id.busid);
        EditText busnum = (EditText) findViewById(R.id.busnum);
        new AlertDialog.Builder(this)
                .setTitle("버스차량번호 확인")
                .setMessage(busid.getText()+"\n"+busnum.getText()+"번 버스가 맞으십니까?")
                .setIcon(android.R.drawable.ic_menu_save)
                .setPositiveButton(android.R.string.yes, (dialogInterface, i) -> {
                    test1.setText(BuscheckId(String.valueOf(busid.getText())));
                    //이거 실행후 이제 다른창으로 가서 서버에 있는 버스 번호와 동일한지 확인하기
                    NetworkBus.setDriverUID("234");
                    NetworkBus.setDriverName("김태욱");
                    NetworkBus.setDriverRouteNo(String.valueOf(busnum));
                    NetworkBus.setDriverVehicleNo(String.valueOf(busid));
                    if(NetworkBus.login() == false){
                        return;
                    }
                    Intent intent = new Intent(this,BD_loginActivity.class);
                    startActivity(intent);
                })
                .setNegativeButton(android.R.string.no, (dialogInterface, i) -> Toast.makeText(getApplicationContext(),"취소하였습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show()).show();
    }
    /*public void join_Click(View view){
        Intent intent = new Intent(this,JoinActivity.class);
        startActivity(intent);
    }*/

    public String BuscheckId(String id){
        String tmpid = id;
        if(tmpid.replace(" ","").equals("")){
            Toast.makeText(getApplicationContext(),"공백만 입력되었습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show();
        }
        else
        {
            tmpid = tmpid.replace(" ", "");
            return tmpid;
        }
        return null;
    }
}
