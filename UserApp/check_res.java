package com.djy.budy;

import static android.speech.tts.TextToSpeech.ERROR;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.Vibrator;
import android.speech.tts.TextToSpeech;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class check_res extends AppCompatActivity {
    private TextToSpeech tts;
    TextView result;
    Vibrator vibrator;
    private Thread waitVibeThread;

    @SuppressLint("HandlerLeak")

    final Handler ui_handler = new Handler(){
        @Override
        public void handleMessage(Message msg){
            if(msg.what == 1){
                vibrator.vibrate(1000);
                tts.speak(LoginActivity.identify + "번 버스가 오는 중입니다 이용해주셔서 감사합니다", TextToSpeech.QUEUE_FLUSH,null);
                Intent intent = new Intent(check_res.this, MainActivity.class); //gps를 찾는 화면으로
                startActivity(intent);
                finish();
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_res);

        Button cancel = (Button) findViewById(R.id.cancel);
        vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        result=(TextView) findViewById(R.id.reserch); //이거 텍스트뷰 큰 화면으로
        String text_coming = LoginActivity.identify + "번 버스가 오는 중입니다.";
        result.setText(text_coming);

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        cancel.setOnClickListener(new DoubleClickListener() {
            @Override
            public void onDoubleClick() {
                Network.cancelBus();
                Intent intent = new Intent(check_res.this,MainActivity.class); //버스 찾는 버튼으로 이동
                tts.speak("예약이 취소되었습니다.", TextToSpeech.QUEUE_FLUSH,null);
                startActivity(intent);
            }

            @Override
            public void onSingleClick() {
                tts.speak("예약을 취소하시겠습니까? 취소하시려면 버튼을 더블클릭해주세요.", TextToSpeech.QUEUE_FLUSH,null);
            }
        });

        Thread th = new Thread(){
            public void run(){
                boolean result = Network.waitVIBE();
                Message msg = ui_handler.obtainMessage();
                if(result){
                    msg.what = 1;
                }else{
                    msg.what = 0;
                }
                ui_handler.sendMessage(msg);
            }
        };

        th.start();
    }
}