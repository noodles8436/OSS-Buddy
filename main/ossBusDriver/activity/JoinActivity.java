package com.example.realbusdriver;

import android.app.AlertDialog;
import android.content.Intent;
import android.net.Network;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class JoinActivity extends AppCompatActivity{
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join);
    }
    public void joinbtn_Click(View view){
        EditText bdname=(EditText) findViewById(R.id.name);
        EditText bdtel=(EditText) findViewById(R.id.busdnum);
        new AlertDialog.Builder(this)
                .setTitle("회원가입")
                .setMessage(bdname.getText()+"\n"+bdtel.getText()+"로 회원가입하시겠습니까?")
                .setIcon(android.R.drawable.ic_menu_save)
                .setPositiveButton(android.R.string.yes, (dialogInterface, i) -> {
                    NetworkBus.setDriverName(bdname.getText().toString());
                    NetworkBus.setDriverUID(bdtel.getText().toString());
                    NetworkBus.setDriverVehicleNo("강원12자3948");
                    NetworkBus.register();
                    Intent intent = new Intent(this,MainActivity.class);
                    startActivity(intent);
                })
                .setNegativeButton(android.R.string.no, (dialogInterface, i) -> Toast.makeText(getApplicationContext(),"취소하였습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show()).show();
    }
}
