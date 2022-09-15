package com.djy.budy;
//회원가입 구현

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Main2Activity extends AppCompatActivity {

    private EditText email_join;
    private EditText pwd_join;
    private EditText phone_join,name_join;
    private Button btn;
    FirebaseAuth firebaseAuth;
    private FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
    private DatabaseReference databaseReference = firebaseDatabase.getReference();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join); //회원가입
        email_join = (EditText) findViewById(R.id.sign_up_email);
        pwd_join = (EditText) findViewById(R.id.sign_up_pwd);
        phone_join=(EditText)findViewById(R.id.sign_up_phone);
        name_join=(EditText)findViewById(R.id.sign_up_name);
        btn = (Button) findViewById(R.id.sign_up_btn);


        firebaseAuth = FirebaseAuth.getInstance();
        FirebaseUser currentFirebaseUser = FirebaseAuth.getInstance().getCurrentUser() ;

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String email = email_join.getText().toString().trim();
                final String pwd = pwd_join.getText().toString().trim();
                final String phone = phone_join.getText().toString().trim();
                final String name = name_join.getText().toString().trim();
                //공백인 부분을 제거하고 보여주는 trim()

                firebaseAuth.createUserWithEmailAndPassword(email, pwd)
                        .addOnCompleteListener(Main2Activity.this, new OnCompleteListener<AuthResult>() {
                            @Override
                            public void onComplete(@NonNull Task<AuthResult> task) {

                                if (task.isSuccessful()) {
                                    Intent intent = new Intent(Main2Activity.this, MainActivity.class);
                                    startActivity(intent);
                                    Network.setUserUID(currentFirebaseUser.getUid());
                                    Network.setUserName("도주영");
                                    Network.setUserPhone("01035302274");
                                    Network.register();
                                }
                                else {
                                    Toast.makeText(Main2Activity.this, "등록 에러", Toast.LENGTH_SHORT).show();
                                    return;
                                }
                            }
                        });
            }
        });



    }
}