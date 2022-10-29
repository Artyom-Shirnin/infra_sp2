import os
import re

from django.conf import settings


class TestDockerfile:

    def test_dockerfile(self):
        try:
            with open(f'{os.path.join(settings.BASE_DIR, "Dockerfile")}', 'r') as f:
                dockerfile = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что файл Dockerfile существует'

        assert re.search(r'FROM\s+python:', dockerfile), (
            'Проверьте, что в файл Dockerfile добавлена инструкция FROM с указанием образа python'
        )
        assert re.search(r'((RUN)|(&&))\s+pip(3|)\s+install\s+-r.+requirements\.txt', dockerfile), (
            'Проверьте, что в Dockerfile добавлена инструкция RUN с установкой зависимостей '
            'из файла requirements.txt'
        )
