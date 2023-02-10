# BankruptcyAPP

Project consists of:
  * Client-side - ReactJS
  * Server-side for doing data analysis and Prediction models - Python Flask
  * Server-side for database, to store created prediction model data- .Net (added later when there will be fully working logistic reggresion model on python server-side)
  
Flow of project:
  1. Create api to do bussiness logic with data, logistic reggresion model
  2. Create server side to display results achieved with data
  3. In parallel work on client-side and python server-side until a full automized Logit model is made
  4. Add .Net project (scrap parts of previous project) to store results from python server-side
  5. Add a Self-Organizing Map and Binary Tree models to the api 

ToDo:
 * Fix bugs for full correlation:
  * On some cases Full correlation doesn't take variables only by full correlation
 
Issues to fix:
 * Fix errors caused by faulty columns in the method singleLogit

Screenshots of Webpage:

MainPage:
![image](https://user-images.githubusercontent.com/85391870/216516539-0312ef49-3e0d-4f3a-93f9-81fac7baf8d1.png)

CreateModel Page:
 * PreModel
 ![image](https://user-images.githubusercontent.com/85391870/216517095-70fe9d28-b328-489f-a720-c1fb6981cd8a.png)
 * Created Model Variable Statistics
 ![image](https://user-images.githubusercontent.com/85391870/216516649-7f853c48-7e23-417b-819d-bb13cad01c17.png)
 * Created Model Correlations
 ![image](https://user-images.githubusercontent.com/85391870/216516693-02f13135-65d1-40cf-9961-5857be62dff2.png)
 * Created Model Generated Model
 ![image](https://user-images.githubusercontent.com/85391870/216516818-c151f1f6-1896-41e3-b2e9-832607e667a2.png)
 ![image](https://user-images.githubusercontent.com/85391870/216516848-6ee9cd2c-9306-4b0d-82a4-cf5dc53ac1fe.png)
 * Created Model Generated Model's subModel with removed correlations
 ![image](https://user-images.githubusercontent.com/85391870/216516913-1760d26a-9be1-4a87-a76f-3091d2435095.png)
 ![image](https://user-images.githubusercontent.com/85391870/216516938-3a3a16f3-23d8-4b98-8cde-57eae41c24c7.png)
