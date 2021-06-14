from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db
from flask_login import current_user, login_required
from app.usuarios.utilidades import check_confirmed 
from .models import Docente, ComentarioDocente
from .forms import AdicionarDocente, AdicionarComDocente, AdicionarDocente

docentes = Blueprint('docentes', __name__)
# pagina da lista de docentes
# pagina do docente especifico
# pagina para editar docentes
# pagina (modal) para deletar docente

@docentes.route('/docente', methods=['GET','POST'])
@login_required
@check_confirmed
def docente():
    page = request.args.get('page', 1, type=int)
    doces = Docente.query.order_by(Docente.id).paginate(page=page, per_page=5)

    form = AdicionarDocente()
    if form.validate_on_submit():
        doce = Docente(
                        nome=form.nome.data.lower().title(), 
                        email=form.email.data,
                        siape=form.siape.data,
                        dep=form.dep.data.lower().title(), 
                        link_ufrj=form.link.data)
        db.session.add(doce)
        db.session.commit()

        flash('Docente cadastrado com sucesso!', 'success')
        return redirect(url_for('docentes.docente'))
    return render_template('docente/docente.html', title='Docentes', doces=doces, form=form)

@docentes.route('/docentes/<int:docente_id>', methods=['GET','POST'])
@login_required
@check_confirmed
def docente_esp(docente_id):
    doce = Docente.query.get_or_404(docente_id)

    coms = ComentarioDocente.query.filter_by(doce_id=docente_id).all()
    form = AdicionarComDocente()
    if form.validate_on_submit():
        com = ComentarioDocente(
                        doce_id=doce.id, 
                        conteudo=form.conteudo.data,
                        nome_usuario=current_user.nome_usuario)
        db.session.add(com)
        db.session.commit()

        flash('Comentário feito com sucesso!', 'success')
        return redirect(url_for('docentes.docente_esp', docente_id=doce.id))
    
    return render_template('docente/docente_esp.html', title="Docente", doce=doce, form=form, coms=coms)

@docentes.route('/docente/<int:docente_id>/editar', methods=['GET','POST'])
@login_required
@check_confirmed
def editar_docente(docente_id):
    doce = Docente.query.get_or_404(docente_id)

    if not current_user.admin:
        redirect(url_for('docentes.docentes'))

    form = AdicionarDocente()
    if form.validate_on_submit():
        doce.nome = form.nome.data.lower().title()
        doce.siape = form.siape.data
        doce.email = form.email.data
        doce.dep = form.dep.data.lower().title()
        doce.link_ufrj = form.link.data
        db.session.commit()
        flash('Docente atualizado!', 'success')
        return redirect(url_for('docentes.docente', post_id=doce.id))

    elif request.method == 'GET':
        form.nome.data = doce.nome
        form.siape.data = doce.siape
        form.dep.data = doce.dep
        form.email.data = doce.email
        form.link.data = doce.link_ufrj
    return render_template('docente/editar_docente.html', title="Docente", form=form)

@docentes.route('/editar_docente/<int:docente_id>/deletar', methods=['GET','POST'])
@login_required
@check_confirmed
def deletar_docente(docente_id):
    doce = Docente.query.get_or_404(docente_id)

    if not current_user.admin:
        redirect(url_for('docentes.docente'))

    db.session.delete(doce)
    db.session.commit()
    flash('Docente deletado!', 'success')
    return redirect(url_for('docentes.docente'))