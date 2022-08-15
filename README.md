# workstation-backend

Back-End of Workstation Project

## Run file Linux

```python
pip install -r requirements.txt
cd app
gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

## Todo

- [ ] Documentation
- [ ] Minor fixes
- [ ] Create sql static data boxes
- [X] New way to send email
- [ ] New html inside emails
- [ ] Deploy

## References

- [Email html template](https://beefree.io/templates/)
