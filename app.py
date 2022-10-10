from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)


#global return_recent
return_recent=0
#global return_rows
return_rows=0

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content= db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        #print (task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'issue happened'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        
        #print the must recent entered element
        #global recent
        recent=0
        #global rows
        rows = Todo.query.count()
        if rows!=0:
            recent=tasks[-1].content

        print ('number of rows=',rows)
        
        print('most recent entered=',recent)

        #print sum of the data base
        sum=0
        if rows!=0:
            for task in tasks:
                sum=sum+int(task.content)

        print ('sum=',sum)
        
        
        global return_rows
        return_rows=rows
        global return_recent
        return_recent=recent
        data_return()

        return render_template('index.html',tasks=tasks,sum_web=sum,recent_fed=recent)


def data_return ():
    tasks=Todo.query.order_by(Todo.date_created).all()
    
    recent=0

    rows = Todo.query.count()
    if rows==1:
        #recent=tasks[0].content
        recent=0
    elif rows!=0 and rows!=1:
        recent=tasks[-1].content

    #print ('data_return func rows=',rows)
        
    #print('data_return func recent=',recent)
    
    #recent_val=return_recent
    #length=return_rows
    #print("data_return func, recent_val=",recent_val)
    #print("data_return func, length=",length)
    
    return recent,rows


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'error happened with deleting'

@app.route('/delete_all/')
def delete_all():
    tasks=Todo.query.order_by(Todo.date_created).all()
    
    try:

        for task in tasks:
            all_delete=Todo.query.get_or_404(task.id)
            db.session.delete(all_delete)
            db.session.commit()

        return redirect('/')
    except:
        return 'error happened with deleting all'
    



@app.route('/update/<int:id>',methods=['Get','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'update issue happened'
    else:
        return render_template('update.html',task=task)


if __name__=="__main__":
        app.run(debug=True)
        data_return()