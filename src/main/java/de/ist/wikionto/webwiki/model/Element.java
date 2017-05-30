/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki.model;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author Marcel
 */
public class Element extends NamedElement{
    
    private final Set<String> categories;
    
    public Element(){
        categories = new HashSet<>();
    }

    /**
     * @return the types
     */
    public Set<String> getCategories() {
        return Collections.unmodifiableSet(categories);
    }
    
    public void addCategory(String classifier){
        if(classifier.contains("|"))
            System.err.println(getName()+" flawed with category:"+classifier);
        categories.add(classifier);
    }
    
}
