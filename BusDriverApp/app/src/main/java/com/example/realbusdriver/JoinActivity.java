package com.example.realbusdriver;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.RandomAccessFile;
import java.util.Random;
import java.util.RandomAccess;

public class JoinActivity extends AppCompatActivity{



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join);
    }
    //회원가입 버튼을 눌렀을 때
    public void joinbtn_Click(View view){
        EditText bdname=(EditText) findViewById(R.id.name);
        EditText vehicle=(EditText) findViewById(R.id.vehiclenum);
        EditText routenum=(EditText)findViewById(R.id.routenum);
        new AlertDialog.Builder(this)
                .setTitle("회원가입")
                .setMessage("이름:"+bdname.getText()+"\n"+vehicle.getText()+"\n"+routenum.getText()+"로 회원가입하시겠습니까?")
                .setIcon(android.R.drawable.ic_menu_save)
                .setPositiveButton(android.R.string.yes, (dialogInterface, i) -> {
                    //버스기사 UID생성
                    Random random=new Random();
                    long UID_first=random.nextInt(9999)+1;
                    long UID_second=random.nextInt(999999)+1;

                    String UID= String.valueOf(UID_first)+UID_second;
                    String busDriverName = bdname.getText().toString();
                    String busVehicleNo = BuscheckId(vehicle.getText().toString());
                    String busRouteNo = routenum.getText().toString();


                    //서버에 정보 넘겨주기
                    NetworkBus.setDriverName(busDriverName);
                    NetworkBus.setDriverVehicleNo(busVehicleNo);
                    NetworkBus.setDriverRouteNo(busRouteNo);
                    NetworkBus.setDriverUID(UID);
                    NetworkBus.register();
                    MainActivity.saveBD.saveBusDriver(busDriverName, UID, busVehicleNo, busRouteNo);

                    Intent intent = new Intent(this,MainActivity.class);
                    startActivity(intent);
                })
                .setNegativeButton(android.R.string.no, (dialogInterface, i) -> Toast.makeText(getApplicationContext(),"취소하였습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show()).show();
    }
    //버스차량번호 입력받을 때, 빈칸 없애고 공백일 경우 오류띄우기
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
