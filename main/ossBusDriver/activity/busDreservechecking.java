package com.example.realbusdriver;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

public class BD_loginActivity extends AppCompatActivity {

    private Thread getReserveThread = null;
    private boolean isRunThread = false;
    private BusReserve busReserve = null;

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bdlogin);
        TextView busstop=(TextView) findViewById(R.id.busstopname);
        TextView prebus=(TextView) findViewById(R.id.prebus);
        TextView busdrivername=(TextView) findViewById(R.id.busdrivername);
        TextView busroutenum=(TextView) findViewById(R.id.busnumber);
        busroutenum.setText(NetworkBus.getDriverRouteNo()+"번 버스 운행");
        busdrivername.setText("버스기사이름: "+NetworkBus.getDriverName()+"기사님");

        busstop.post(new Runnable() {
            @Override
            public void run() {
                if(busReserve == null){
                    busstop.setText("예약한 사람이 없습니다.");
                }else{
                    busstop.setText("정거장 이름: "+ busReserve.getStationName() +" 에 예약한 사람이 있습니다.");
                }
            }
        });

        prebus.post(new Runnable() {
            @Override
            public void run() {
                if(busReserve == null){
                    prebus.setText("");
                }else{
                    prebus.setText(busReserve.getArrivalLeftNode() + "뒤에 예약한 사람이 있습니다.");
                }
            }
        });

        getReserveThread = new Thread(){
            public void run(){
                isRunThread = true;
                while (isRunThread){
                     busReserve = NetworkBus.getReserveStation();
                }
            }
        };

        runThread();

    }

    private void runThread(){
        getReserveThread.start();
    }

    private void stopThread(){
        isRunThread = false;
    }
}
