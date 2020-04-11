from django.db import transaction

from exceptions import NotEnoughMoney
from .models import AccountUser
from .forms import TransferForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView


@transaction.atomic  # Cancel all db operations in case of error during view execution.
class TransferView(FormView):
    
    form_class = TransferForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()

        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()
        amount = request.POST['amount']

        # Find target users using their tax_ids
        target_users = AccountUser.objects.filter(inn=request.POST['inn_to'])

        if target_users.exists():
            user = AccountUser.objects.select_related('accounts', 'user').get(id=request.POST['user_from'])
            user_account = user.accounts.filter(amount_gte=amount).first()

            # Withdraw money or return error if there's not enough
            try:
                user_account.withdraw(amount=amount)
            except NotEnoughMoney:
                ctx['op_result'] = 'На счёте недостаточно средств'
                return self.render_to_response(ctx)

            # Top up target users' accounts
            top_up_amount = amount / target_users.count()
            for target_user in target_users:
                target_user.top_up(top_up_amount=top_up_amount)
        else:
            ctx['op_result'] = 'Перевод не выполнен, не найдены реципиенты.'

        return self.render_to_response(ctx)

    def userlist(self):
        user_list = []
        for i in User.objects.all():
            cur_user = {}
            cur_user['id'] = i.id
            cur_user['username'] = i.username
            if i.users_set.all():
                tmp = i.users_set.get()
                cur_user['inn'] = tmp.inn
                cur_user['account'] = tmp.account
            user_list.append(cur_user)
        return user_list
