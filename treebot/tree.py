import yaml

TREE = yaml.load("""
say: "What is the purpose of your visit? (options: travel, study, business/work, medical treatment, join family/get married, visit child at school, diplomatic/government visit)"
answers:
  travel:
    say: You need a Standard Visitor Visa
  study:
    say: How long are you going to stay in the UK? up to 6 months; more than 6 months
    answers:
      up to 6 months:
        say: You can apply for a Short-term Study Visa
      more than 6 months:
        say: You need a Study Visa (Tier 4)
  business/work:
    say: How long are you going to stay in the UK? up to 6 months; more than 6 months
    answers:
      up to 6 months:
        say: You need a Standard Visitor Visa
      more than 6 months:
        say: Are you an 1. entrepreneur 2.investor 3. leader in arts or sciences 4. none of the above
        answers:
          '1':
            say: You can apply for a Tier 1 Entrepreneur
          '2':
            say: You can apply for Tier 1 Investor
          '3':
            say: You can apply for Tier 1 (Exceptional Talent)
          '4':
            say: Are you offered  1. a skilled job 2. role in the UK branch of your employer 3. job in a religious community 4. job as an elite sportsman or coach
            answers:
              '1':
                say: You can apply for a Tier 2 (General) visa
              '2':
                say: You can apply for a Tier 2 (Intra-company transfer)
              '3':
                say: Tier 2 (Minister of Religion)
              '4':
                say: Tier 2 (Sportsperson)
  medical treatment:
    say: You need a Standard Visitor Visa
  join family/get married:
    say: You need a Family of a settled person visa if your family/partner are settled in the UK or a 'dependant' visa of their visa category if they are working or studying
  visiting a child:
    say: You need a Parent visa if you're visiting for over 6 months and a Standard Visitor visa if your visit is  for less than 6 months
  diplomatic or government visit:
    say: You can apply for exempt vignette (exempt from immigration control)
""")
