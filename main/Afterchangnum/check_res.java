package com.example.ynbutton;

import android.content.Context;
import android.content.Intent;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class check_res extends AppCompatActivity {
    private TextToSpeech tts;
    TextView result;
    Vibrator vibrator;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_res);
        Button cancel = (Button) findViewById(R.id.cancel);
        vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        result=(TextView) findViewById(R.id.reserch); //이거 텍스트뷰 큰 화면으로
        //버스 에약하는 버튼있는 레이아웃
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.이전레이아웃);
        View view = inflater.inflate(R.layout.이전레이아웃);
        //버스 예약하는 화면에 있는 버튼 정보가져오기 위한 용도
        Button busname = (Button) view.findViewById(R.id.reservation);
        result.setText(busname.getText()+"가 오는 중입니다.");
        cancel.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                Network.cancelBus();
                Intent intent = new Intent(this,changebusnum.class); //버스 찾는 버튼으로 이동
                startActivity(intent);
            }

            @Override
            public void onSingleClick() {
                tts.speak(result.getText().toString()+"예약을 취소하시겠습니까? 취소하시려면 버튼을 2번눌려주세요", TextToSpeech.QUEUE_FLUSH,null);
            }
        });

        if(Network.waitVIBE()){
            vibrator.vibrate(500);
            tts.speak("이용해주셔서 감사합니다.", TextToSpeech.QUEUE_FLUSH,null);
            Intent intent = new Intent(this,gps.class); //gps를 찾는 화면으로
            startActivity(intent);
        }

    }

}
