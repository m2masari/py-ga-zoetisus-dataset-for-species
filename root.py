import shutil


def main():

    from reports import behavior
    from reports.conversions import goals
    from reports.audience import geo
    from reports.audience import technology
    from reports.audience import mobile
    from reports.audience import demographics
    from reports.audience import behavior
    from reports.acquisition import alltraffic
    from reports.acquisition import campaigns

    from reports import concatenate
    concatenate.concatenate()

    shutil.rmtree(path=r"C:\Users\melik.masarifoglu\Documents\species")
    shutil.copytree(src=r"C:\Users\melik.masarifoglu\PycharmProjects\py-ga-zoetisus-dataset-for-species\_exports",
                    dst=r"C:\Users\melik.masarifoglu\Documents\species",
                    dirs_exist_ok=True)

    return


if __name__ == '__main__':
    main()
#else:
#    raise RuntimeError("{name} can't be imported!".format(name=__file__))
