package com.example.ynbutton;

import static android.speech.tts.TextToSpeech.ERROR;

import android.content.Context;
import android.content.Intent;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import com.example.ynbutton.Network;

import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private TextToSpeech tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        //이전레이아웃자리에 이 화면으로 넘어오기 전 레이아웃을 입력하면 됩니다.
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.이전레이아웃);
        View view = inflater.inflate(R.layout.이전레이아웃);
        //이전레이아웃에 있는 id:reservation을 가진 버튼을 가져옵니다.
        Button busname = (Button) view.findViewById(R.id.reservation);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != ERROR) {
                    // 언어를 선택한다.
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });
        Button ybutton = (Button) findViewById(R.id.yesbutton);
        Button nbutton = (Button) findViewById(R.id.nobutton);
         ybutton.setOnClickListener(new DoubleClickListener() {
             @Override
             public void onDoubleClick() {
                 Intent intent = new Intent(this,//에약중이라는 걸 띄우는 레이아웃.class);
                  Network.reserveBus(busname.getText().toString());//버스 노선번호 가져오기
                 startActivity(intent);
             }

             @Override
             public void onSingleClick() {
                 tts.speak(busname.getText().toString()+"이 맞으십니까? 맞다면 이 부분을 더블클릭해주세요", TextToSpeech.QUEUE_FLUSH,null);
             }
         });
         nbutton.setOnClickListener(new DoubleClickListener() {
             @Override
             public void onDoubleClick() {
                 //Intent intent = new Intent(this,//버스 예약버튼 띄우는 레이아웃.class);
                 startActivity(intent);
             }

             @Override
             public void onSingleClick() {
                 tts.speak(busname.getText().toString()+"이 아니십니까? 예약하고자 하는 버스가 아니라면 이 부분을 더블클릭해주세요", TextToSpeech.QUEUE_FLUSH,null);
             }
         });
    }
}
