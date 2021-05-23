from flask import render_template, flash, redirect, url_for, request, Blueprint
from .models import Doc
from app import db
from flask_login import current_user, login_required
from app.decoradores import check_confirmed
from .models import Doc
from .forms import AdicionarDoc

documentos = Blueprint('documentos', __name__)

@documentos.route('/documento', methods=['GET','POST'])
@login_required
@check_confirmed
def documento():
    # quantidade de documentos a ser mostrado no site
    # incluir forma de iterar sobre os diferentes blocos
    # descobrir como fzr slicing da database
    page = request.args.get('page', 1, type=int)
    docs = Doc.query.order_by(Doc.id).paginate(page=page, per_page=5)

    form = AdicionarDoc()
    if form.validate_on_submit():
        doc = Doc(
                        titulo=form.titulo.data, 
                        autor=form.autor.data,
                        tipo=form.tipo.data, 
                        formato=form.formato.data,  
                        link=form.link.data)
        db.session.add(doc)
        db.session.commit()

        flash('Documento cadastrado com sucesso!', 'success')
        return redirect(url_for('documento.documento'))
    return render_template('documento/documento.html', title='Documentos', docs=docs, form=form)

@documentos.route('/documento/<int:documento_id>', methods=['GET','POST'])
@login_required
@check_confirmed
def documento_esp(documento_id):
    doc = Doc.query.get_or_404(documento_id)
    return render_template('documento/documento_esp.html', title="Documento", doc=doc)

@documentos.route('/documento/<int:documento_id>/editar', methods=['GET','POST'])
@login_required
@check_confirmed
def editar_documento(documento_id):
    doc = Doc.query.get_or_404(documento_id)

    if not current_user.admin:
        redirect(url_for('documento.documento'))

    form = AdicionarDoc()
    if form.validate_on_submit():
        doc.titulo = form.titulo.data
        doc.autor = form.autor.data
        doc.tipo = form.tipo.data
        doc.formato = form.formato.data
        doc.link = form.link.data
        db.session.commit()
        flash('Documento atualizado!', 'success')
        return redirect(url_for('documento.documento', post_id=doc.id))

    elif request.method == 'GET':
        form.titulo.data = doc.titulo
        form.autor.data = doc.autor
        form.tipo.data = doc.tipo
        form.formato.data = doc.formato
        form.link.data = doc.link
    return render_template('documento/editar_documento.html', title="Documento", form=form)

@documentos.route('/editar_documento/<int:documento_id>/deletar', methods=['GET','POST'])
@login_required
@check_confirmed
def deletar_documento(documento_id):
    doc = Doc.query.get_or_404(documento_id)

    if not current_user.admin:
        redirect(url_for('documento.documento'))

    db.session.delete(doc)
    db.session.commit()
    flash('Documento deletado!', 'success')
    return redirect(url_for('documento.documento'))
   