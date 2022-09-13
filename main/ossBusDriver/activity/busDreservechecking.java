package com.example.busdreservechecking;

import android.annotation.SuppressLint;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView busstop=(TextView) findViewById(R.id.busstopname);
        TextView prebus=(TextView) findViewById(R.id.prebus);
    while (true){
        busstop.setText("정거장 이름: "+NetworkBus.getReserveStation().getStationName()+"에 예약한 사람이 있습니다.");
        prebus.setText(NetworkBus.getReserveStation().getArrivalLeftNode()+"뒤에 예약한 사람이 있습니다.");
    }

    }
}
