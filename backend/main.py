from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models import Post

app = FastAPI(title="Workshop Docker - FastAPI + Postgres")

# Cria as tabelas no banco de dados na inicialização
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Schema de entrada (o que o usuário envia)
class PostCreate(BaseModel):
    title: str
    content: str


# Rota principal - exibe todos os posts em HTML
@app.get("/", response_class=HTMLResponse)
def read_root(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).all()

    posts_html = ""
    for post in posts:
        posts_html += f"""
        <div class="post-card">
            <h2>{post.title}</h2>
            <p>{post.content}</p>
            <small>ID: {post.id}</small>
        </div>
        """

    if not posts_html:
        posts_html = '<p class="empty">Nenhum post ainda. Crie o primeiro!</p>'

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Workshop Docker</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                min-height: 100vh;
                padding: 2rem;
            }}
            header {{
                text-align: center;
                margin-bottom: 2.5rem;
            }}
            header h1 {{
                font-size: 2.5rem;
                background: linear-gradient(135deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            header p {{ color: #94a3b8; margin-top: 0.5rem; }}
            .container {{ max-width: 700px; margin: 0 auto; }}
            form {{
                background: #1e293b;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 2rem;
                border: 1px solid #334155;
            }}
            form h2 {{ margin-bottom: 1rem; color: #38bdf8; }}
            input, textarea {{
                width: 100%;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: 1px solid #334155;
                background: #0f172a;
                color: #e2e8f0;
                font-size: 1rem;
                margin-bottom: 0.75rem;
                outline: none;
                transition: border-color 0.2s;
            }}
            input:focus, textarea:focus {{ border-color: #38bdf8; }}
            textarea {{ resize: vertical; min-height: 100px; }}
            button {{
                background: linear-gradient(135deg, #38bdf8, #818cf8);
                color: #0f172a;
                font-weight: bold;
                padding: 0.75rem 2rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
                transition: opacity 0.2s;
            }}
            button:hover {{ opacity: 0.85; }}
            .post-card {{
                background: #1e293b;
                border-radius: 12px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1rem;
                border: 1px solid #334155;
                transition: transform 0.2s;
            }}
            .post-card:hover {{ transform: translateY(-2px); }}
            .post-card h2 {{ color: #38bdf8; margin-bottom: 0.5rem; }}
            .post-card p {{ color: #cbd5e1; line-height: 1.6; }}
            .post-card small {{ color: #64748b; display: block; margin-top: 0.5rem; }}
            .empty {{ color: #64748b; text-align: center; padding: 2rem; }}
            #msg {{ color: #4ade80; margin-top: 0.5rem; font-size: 0.9rem; min-height: 1.2rem; }}
        </style>
    </head>
    <body>
        <header>
            <h1>🐳 Workshop Docker</h1>
            <p>FastAPI + PostgreSQL + Docker</p>
        </header>
        <div class="container">
            <form id="postForm">
                <h2>✏️ Criar Post</h2>
                <input type="text" id="title" placeholder="Título do post" required />
                <textarea id="content" placeholder="Conteúdo do post..." required></textarea>
                <button type="submit">Publicar</button>
                <div id="msg"></div>
            </form>
            <h2 style="margin-bottom:1rem; color:#94a3b8;">📋 Posts</h2>
            {posts_html}
        </div>
        <script>
            document.getElementById('postForm').addEventListener('submit', async (e) => {{
                e.preventDefault();
                const msg = document.getElementById('msg');
                const title = document.getElementById('title').value;
                const content = document.getElementById('content').value;
                try {{
                    const res = await fetch('/posts', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ title, content }})
                    }});
                    if (res.ok) {{
                        msg.textContent = '✅ Post criado com sucesso!';
                        setTimeout(() => location.reload(), 800);
                    }} else {{
                        msg.textContent = '❌ Erro ao criar post.';
                    }}
                }} catch (err) {{
                    msg.textContent = '❌ Erro de conexão.';
                }}
            }});
        </script>
    </body>
    </html>
    """


# Rota para criar um post
@app.post("/posts", status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"id": db_post.id, "title": db_post.title, "content": db_post.content}


# Rota para listar todos os posts (API JSON)
@app.get("/posts")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).all()
    return posts
