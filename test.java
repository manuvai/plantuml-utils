package entities;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;
import java.util.Set;

@Entity
@Table(name = "Employe")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "TypeE", discriminatorType = DiscriminatorType.STRING)
@DiscriminatorValue("Employe")
public class Employe implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer codeE;

    @Column(name = "NomE")
    private String nom;

    @Column(name = "prenomE")
    private String prenom;

    @OneToMany(mappedBy = "employe", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    private Set<Demande> demandes;

    @ManyToMany
    @JoinTable(name = "Travailler",
            joinColumns = @JoinColumn(name = "CodeEmp"),
            inverseJoinColumns = @JoinColumn(name = "CodeServ"))
    private Set<Service> services;

    public Employe() {
    }

    public Employe(String inNom, String inPrenom) {
        setNom(inNom);
        setPrenom(inPrenom);
    }

    public Integer getCodeE() {
        return codeE;
    }

    public void setCodeE(Integer codeE) {
        this.codeE = codeE;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public String getPrenom() {
        return prenom;
    }

    public void setPrenom(String prenom) {
        this.prenom = prenom;
    }

    public Set<Demande> getDemandes() {
        return demandes;
    }

    public void setDemandes(Set<Demande> demandes) {
        this.demandes = demandes;
    }

    public Set<Service> getServices() {
        return services;
    }

    public void setServices(Set<Service> services) {
        this.services = services;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Employe)) return false;
        Employe employe = (Employe) o;
        return Objects.equals(getCodeE(), employe.getCodeE())
                && Objects.equals(getNom(), employe.getNom())
                && Objects.equals(getPrenom(), employe.getPrenom())
                && Objects.equals(getDemandes(), employe.getDemandes());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getCodeE(), getNom(), getPrenom(), getDemandes());
    }

    @Override
    public String toString() {
        return "Employe{" +
                "codeE=" + codeE +
                ", nom='" + nom + '\'' +
                ", prenom='" + prenom + '\'' +
                ", demandes=" + getDemandes() +
                '}';
    }

    private void smth() {
        
    }
}
