package com.example.busdriver;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity{


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void btn_Click(View view) {
        TextView test1 = (TextView) findViewById(R.id.test1);
        EditText busid = (EditText) findViewById(R.id.busid);
        String tmpid = String.valueOf(busid.getText());
        new AlertDialog.Builder(this)
                .setTitle("버스차량번호 확인")
                .setMessage(tmpid+"로 하시겠습니까?")
                .setIcon(android.R.drawable.ic_menu_save)
                .setPositiveButton(android.R.string.yes, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                    test1.setText(BuscheckId(tmpid));
                    //이거 실행후 이제 다른창으로 가서 서버에 있는 버스 번호와 동일한지 확인하기
                    }
                })
                .setNegativeButton(android.R.string.no, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        Toast.makeText(getApplicationContext(),"취소하였습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show();
                    }
                }).show();
    }
    public String BuscheckId(String id){
        String tmpid = id;
        if(tmpid.replace(" ","").equals("")){
            Toast.makeText(getApplicationContext(),"공백만 입력되었습니다. 다시 입력해주세요",Toast.LENGTH_SHORT).show();
        }
        else if (!tmpid.contains("아") && !tmpid.contains("바") && !tmpid.contains("사")&&!tmpid.contains("자")){
            Toast.makeText(getApplicationContext(),"알맞은 번호가 아닙니다. 다시 입력하세요",Toast.LENGTH_SHORT).show();
        }
        else
        {
            tmpid = tmpid.replace(" ", "");
            return tmpid;
        }
    return null;
    }
}
